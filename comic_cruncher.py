import sys
import os
import zipfile
import rarfile
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import pdf2image
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QProgressBar, QFrame, QTextEdit, QPushButton)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QMimeData, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen, QDragEnterEvent, QDropEvent
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
from functools import partial
import re

def format_file_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"

class ComicCombiner(QThread):
    """Background thread for combining comic issues into TPB collections"""
    
    progress_update = pyqtSignal(str, int)  # stage, percentage
    file_info_update = pyqtSignal(str)  # current file info
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.should_stop = False
    
    def run(self):
        try:
            if len(self.file_paths) < 2:
                self.finished.emit(False, "Need at least 2 files to combine")
                return
            
            self.progress_update.emit("SCANNING", 10)
            
            # Detect series pattern and sort files
            series_info = self.detect_series_pattern(self.file_paths)
            if not series_info:
                self.finished.emit(False, "Could not detect comic series pattern")
                return
            
            series_name = series_info['name']
            sorted_files = series_info['files']
            
            # Split into batches of 12 issues
            batch_size = 12
            batches = []
            for i in range(0, len(sorted_files), batch_size):
                batch = sorted_files[i:i + batch_size]
                batches.append(batch)
            
            self.file_info_update.emit(f"Found {len(sorted_files)} issues, creating {len(batches)} TPB volumes")
            
            total_created = 0
            
            # Process each batch
            for batch_idx, batch_files in enumerate(batches):
                if self.should_stop:
                    return
                
                # Calculate issue range for this batch
                batch_issues = []
                for file_path in batch_files:
                    name = Path(file_path).stem
                    for pattern in [
                        r'(.+?)\s+(\d{3})(?:\s|$)',
                        r'(.+?)\s+Issue\s+(\d+)',
                        r'(.+?)\s+#(\d+)',
                        r'(.+?)\s+(\d+)(?:\s|$)',
                    ]:
                        match = re.search(pattern, name, re.IGNORECASE)
                        if match:
                            batch_issues.append(int(match.group(2)))
                            break
                
                if batch_issues:
                    issue_range = self.format_issue_range(batch_issues)
                    volume_num = batch_idx + 1
                    tpb_name = f"{series_name} Vol {volume_num} (Issues {issue_range}).cbz"
                else:
                    volume_num = batch_idx + 1
                    tpb_name = f"{series_name} Vol {volume_num}.cbz"
                
                output_path = Path(batch_files[0]).parent / tpb_name
                
                # Update progress for this batch
                batch_progress = 20 + int((batch_idx / len(batches)) * 60)
                self.progress_update.emit("COMBINING", batch_progress)
                self.file_info_update.emit(f"Creating Volume {volume_num}: {len(batch_files)} issues")
                
                # Combine all images from this batch
                with tempfile.TemporaryDirectory() as temp_dir:
                    all_images = []
                    
                    for i, file_path in enumerate(batch_files):
                        if self.should_stop:
                            return
                        
                        file_name = Path(file_path).name
                        self.file_info_update.emit(f"Processing: {file_name}")
                        
                        # Extract images from this issue
                        images = self.extract_images_from_comic(file_path, temp_dir, i)
                        all_images.extend(images)
                    
                    if not all_images:
                        self.file_info_update.emit(f"Warning: No images found in Volume {volume_num}")
                        continue
                    
                    # Create combined CBZ for this batch
                    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as tpb:
                        for img_path in sorted(all_images):
                            if os.path.exists(img_path):
                                tpb.write(img_path, os.path.basename(img_path))
                    
                    # Remove original files from this batch
                    for file_path in batch_files:
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Warning: Could not remove {file_path}: {e}")
                    
                    total_created += 1
                    self.file_info_update.emit(f"Completed: {tpb_name}")
            
            self.progress_update.emit("FINALIZING", 100)
            
            if total_created > 1:
                message = f"Created {total_created} TPB volumes from {len(sorted_files)} issues"
            else:
                message = f"Created 1 TPB volume from {len(sorted_files)} issues"
            
            self.finished.emit(True, message)
                
        except Exception as e:
            self.finished.emit(False, f"Combination error: {str(e)}")
    
    def detect_series_pattern(self, file_paths):
        """Detect comic series pattern and extract issue numbers"""
        try:
            comics = []
            for file_path in file_paths:
                name = Path(file_path).stem
                issue_num = None
                series_name = None
                
                # Try multiple patterns for issue detection
                patterns = [
                    r'(.+?)\s+(\d{3})(?:\s|$)',  # Original: "Series Name 001"
                    r'(.+?)\s+Issue\s+(\d+)',     # "Series Name Issue 1"
                    r'(.+?)\s+#(\d+)',           # "Series Name #1"
                    r'(.+?)\s+(\d+)(?:\s|$)',    # "Series Name 1" (fallback)
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, name, re.IGNORECASE)
                    if match:
                        series_name = match.group(1).strip()
                        issue_num = int(match.group(2))
                        break
                
                if series_name and issue_num is not None:
                    comics.append({
                        'path': file_path,
                        'series': series_name,
                        'issue': issue_num,
                        'name': name
                    })
            
            if not comics:
                return None
            
            # Group by series name (take the most common one)
            series_counts = {}
            for comic in comics:
                series = comic['series']
                if series in series_counts:
                    series_counts[series] += 1
                else:
                    series_counts[series] = 1
            
            main_series = max(series_counts, key=series_counts.get)
            series_comics = [c for c in comics if c['series'] == main_series]
            
            # Sort by issue number
            series_comics.sort(key=lambda x: x['issue'])
            
            # Generate range string
            issues = [c['issue'] for c in series_comics]
            range_str = self.format_issue_range(issues)
            
            return {
                'name': main_series,
                'range': range_str,
                'files': [c['path'] for c in series_comics]
            }
            
        except Exception as e:
            print(f"Error detecting series pattern: {e}")
            return None
    
    def format_issue_range(self, issues):
        """Format issue numbers into a readable range string"""
        if not issues:
            return ""
        
        if len(issues) == 1:
            return str(issues[0])
        
        ranges = []
        start = issues[0]
        end = issues[0]
        
        for i in range(1, len(issues)):
            if issues[i] == end + 1:
                end = issues[i]
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = end = issues[i]
        
        # Add the last range
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        
        return ", ".join(ranges)
    
    def extract_images_from_comic(self, file_path, temp_dir, issue_index):
        """Extract images from a comic file"""
        images = []
        try:
            file_path = Path(file_path)
            
            if file_path.suffix.lower() == '.cbz':
                with zipfile.ZipFile(file_path, 'r') as cbz:
                    for filename in sorted(cbz.namelist()):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                            # Extract with unique name
                            original_name = os.path.basename(filename)
                            name, ext = os.path.splitext(original_name)
                            unique_name = f"issue_{issue_index:03d}_{name}{ext}"
                            
                            cbz.extract(filename, path=temp_dir)
                            old_path = os.path.join(temp_dir, filename)
                            new_path = os.path.join(temp_dir, unique_name)
                            
                            os.rename(old_path, new_path)
                            images.append(new_path)
            
            elif file_path.suffix.lower() == '.cbr':
                with rarfile.RarFile(file_path, 'r') as cbr:
                    for filename in sorted(cbr.namelist()):
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                            original_name = os.path.basename(filename)
                            name, ext = os.path.splitext(original_name)
                            unique_name = f"issue_{issue_index:03d}_{name}{ext}"
                            
                            cbr.extract(filename, path=temp_dir)
                            old_path = os.path.join(temp_dir, filename)
                            new_path = os.path.join(temp_dir, unique_name)
                            
                            os.rename(old_path, new_path)
                            images.append(new_path)
        
        except Exception as e:
            print(f"Error extracting from {file_path}: {e}")
        
        return images
    
    def stop(self):
        self.should_stop = True

class ImageProcessor:
    """Handles image processing with parallel execution"""
    
    @staticmethod
    def process_image(image_data, target_size=2500, quality=85):
        """Process a single image: resize and convert to WebP"""
        try:
            if isinstance(image_data, tuple):
                image_path, temp_dir = image_data
                with Image.open(image_path) as img:
                    # Convert to RGB if necessary
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Calculate new size maintaining aspect ratio
                    width, height = img.size
                    if max(width, height) > target_size:
                        if width > height:
                            new_width = target_size
                            new_height = int((height * target_size) / width)
                        else:
                            new_height = target_size
                            new_width = int((width * target_size) / height)
                        
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Save as WebP
                    output_name = Path(image_path).stem + '.webp'
                    output_path = os.path.join(temp_dir, output_name)
                    img.save(output_path, 'WEBP', quality=quality, optimize=True)
                    return output_path
            else:
                # Direct PIL Image object
                img = image_data
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                width, height = img.size
                if max(width, height) > target_size:
                    if width > height:
                        new_width = target_size
                        new_height = int((height * target_size) / width)
                    else:
                        new_height = target_size
                        new_width = int((width * target_size) / height)
                    
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                return img
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

class BatchProcessor(QThread):
    """Background thread for processing multiple comic files"""
    
    progress_update = pyqtSignal(str, int)  # stage, percentage
    file_info_update = pyqtSignal(str)  # current file info
    batch_progress = pyqtSignal(int, int)  # current file, total files
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, file_paths):
        super().__init__()
        self.file_paths = file_paths
        self.should_stop = False
        self.processed_count = 0
        self.skipped_count = 0
        self.error_count = 0
        self.total_space_saved = 0
    
    def run(self):
        try:
            total_files = len(self.file_paths)
            self.file_info_update.emit(f"Starting batch: {total_files} files found")
            
            for i, file_path in enumerate(self.file_paths):
                if self.should_stop:
                    break
                
                self.batch_progress.emit(i + 1, total_files)
                
                # Update with current file being processed
                file_name = Path(file_path).name
                self.file_info_update.emit(f"Processing: {file_name}")
                
                # Process single file
                result = self.process_single_file(file_path)
                
                # Update with result
                if result == "success":
                    self.processed_count += 1
                    self.file_info_update.emit(f"Completed: {file_name}")
                elif result == "skipped":
                    self.skipped_count += 1
                    self.file_info_update.emit(f"Skipped: {file_name} (already crunched)")
                elif isinstance(result, tuple) and result[0] == "error":
                    self.error_count += 1
                    error_detail = result[1]
                    self.file_info_update.emit(f"Error: {file_name} - {error_detail}")
                elif isinstance(result, tuple) and len(result) == 3:
                    # Result with file size info (success, original_size, new_size)
                    self.processed_count += 1
                    original_size, new_size = result[1], result[2]
                    space_saved = original_size - new_size
                    self.total_space_saved += space_saved
                    
                    if original_size > 0:
                        percent_saved = int((space_saved / original_size) * 100)
                        size_info = f"({format_file_size(original_size)} → {format_file_size(new_size)}, {percent_saved}% saved)"
                    else:
                        size_info = ""
                    
                    self.file_info_update.emit(f"Completed: {file_name} {size_info}")
                else:
                    self.error_count += 1
                    self.file_info_update.emit(f"Error: {file_name} (unknown error)")
            
            # Generate summary message
            summary = f"Batch complete! Processed: {self.processed_count}, Skipped: {self.skipped_count}"
            if self.error_count > 0:
                summary += f", Errors: {self.error_count}"
            if self.total_space_saved > 0:
                summary += f" | Space saved: {format_file_size(self.total_space_saved)}"
            
            self.finished.emit(True, summary)
            
        except Exception as e:
            self.finished.emit(False, f"Batch error: {str(e)}")
    
    def process_single_file(self, file_path):
        """Process a single file and return result status"""
        try:
            file_path = Path(file_path)
            
            # Get original file size
            original_size = file_path.stat().st_size
            
            # Check if already crunched
            if self.is_already_crunched(file_path):
                return "skipped"
            
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            
            # Extract images
            if file_path.suffix.lower() == '.pdf':
                images = self.extract_from_pdf(file_path)
            elif file_path.suffix.lower() == '.cbz':
                images = self.extract_from_cbz(file_path)
            elif file_path.suffix.lower() == '.cbr':
                images = self.extract_from_cbr(file_path)
            else:
                return ("error", "Unsupported file format")
            
            if not images:
                return ("error", "No images found in file")
            
            # Process images
            with tempfile.TemporaryDirectory() as temp_dir:
                processed_images = []
                
                if file_path.suffix.lower() == '.pdf':
                    for i, img in enumerate(images):
                        processed_img = ImageProcessor.process_image(img)
                        if processed_img:
                            output_path = os.path.join(temp_dir, f"page_{i:04d}.webp")
                            processed_img.save(output_path, 'WEBP', quality=85, optimize=True)
                            processed_images.append(output_path)
                else:
                    image_tasks = [(img_path, temp_dir) for img_path in images]
                    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                        futures = [executor.submit(ImageProcessor.process_image, task) for task in image_tasks]
                        for future in futures:
                            result = future.result()
                            if result:
                                processed_images.append(result)
                
                if not processed_images:
                    return ("error", "Failed to process any images")
                
                # Create CBZ
                temp_cbz_path = file_path.parent / f"temp_{file_path.stem}.cbz"
                with zipfile.ZipFile(temp_cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz:
                    for img_path in sorted(processed_images):
                        if os.path.exists(img_path):
                            cbz.write(img_path, os.path.basename(img_path))
                
                # Replace original
                final_path = file_path.with_suffix('.cbz') if file_path.suffix.lower() != '.cbz' else file_path
                if final_path.exists():
                    os.remove(final_path)
                os.rename(temp_cbz_path, final_path)
                
                if file_path.suffix.lower() != '.cbz' and file_path.exists():
                    os.remove(file_path)
                
                # Clean up backup
                if backup_path.exists():
                    os.remove(backup_path)
                
                # Get new file size
                new_size = final_path.stat().st_size
                
                return ("success", original_size, new_size)
                
        except PermissionError as e:
            return ("error", f"Permission denied: {str(e)}")
        except FileNotFoundError as e:
            return ("error", f"File not found: {str(e)}")
        except zipfile.BadZipFile as e:
            return ("error", f"Corrupted archive: {str(e)}")
        except Exception as e:
            return ("error", f"Processing failed: {str(e)}")
    
    def stop(self):
        self.should_stop = True
    
    # Copy utility methods from ComicProcessor
    def is_already_crunched(self, file_path):
        """Check if file already contains WebP images"""
        try:
            if file_path.suffix.lower() == '.pdf':
                return False
            elif file_path.suffix.lower() == '.cbz':
                with zipfile.ZipFile(file_path, 'r') as cbz:
                    image_files = [f for f in cbz.namelist() 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'))]
                    if not image_files:
                        return False
                    webp_count = sum(1 for f in image_files if f.lower().endswith('.webp'))
                    return (webp_count / len(image_files)) > 0.8
            elif file_path.suffix.lower() == '.cbr':
                with rarfile.RarFile(file_path, 'r') as cbr:
                    image_files = [f for f in cbr.namelist() 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'))]
                    if not image_files:
                        return False
                    webp_count = sum(1 for f in image_files if f.lower().endswith('.webp'))
                    return (webp_count / len(image_files)) > 0.8
            return False
        except Exception:
            return False
    
    def extract_from_pdf(self, pdf_path):
        try:
            return pdf2image.convert_from_path(pdf_path, dpi=300)
        except Exception:
            return []
    
    def extract_from_cbz(self, cbz_path):
        images = []
        try:
            with zipfile.ZipFile(cbz_path, 'r') as cbz:
                for filename in sorted(cbz.namelist()):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                        cbz.extract(filename, path=tempfile.gettempdir())
                        images.append(os.path.join(tempfile.gettempdir(), filename))
        except Exception:
            pass
        return images
    
    def extract_from_cbr(self, cbr_path):
        images = []
        try:
            with rarfile.RarFile(cbr_path, 'r') as cbr:
                for filename in sorted(cbr.namelist()):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                        cbr.extract(filename, path=tempfile.gettempdir())
                        images.append(os.path.join(tempfile.gettempdir(), filename))
        except Exception:
            pass
        return images

class ComicProcessor(QThread):
    """Background thread for processing comic files"""
    
    progress_update = pyqtSignal(str, int)  # stage, percentage
    file_info_update = pyqtSignal(str)  # file path
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.should_stop = False
    
    def run(self):
        try:
            file_path = Path(self.file_path)
            self.file_info_update.emit(str(file_path))
            
            # Check if file is already crunched (contains WebP images)
            if self.is_already_crunched(file_path):
                self.finished.emit(True, "File already crunched with WebP images!")
                return
            
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            
            # Determine file type and extract images
            if file_path.suffix.lower() == '.pdf':
                images = self.extract_from_pdf(file_path)
            elif file_path.suffix.lower() == '.cbz':
                images = self.extract_from_cbz(file_path)
            elif file_path.suffix.lower() == '.cbr':
                images = self.extract_from_cbr(file_path)
            else:
                self.finished.emit(False, "Unsupported file format")
                return
            
            if not images:
                self.finished.emit(False, "No images found in file")
                return
            
            # Process images in parallel
            with tempfile.TemporaryDirectory() as temp_dir:
                self.progress_update.emit("RESIZING", 10)
                
                # Prepare image processing tasks
                if file_path.suffix.lower() == '.pdf':
                    # For PDF, images are PIL objects
                    processed_images = []
                    total_images = len(images)
                    
                    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                        futures = []
                        for i, img in enumerate(images):
                            future = executor.submit(self.process_pdf_image, img, temp_dir, i)
                            futures.append(future)
                        
                        for i, future in enumerate(futures):
                            if self.should_stop:
                                return
                            result = future.result()
                            if result:
                                processed_images.append(result)
                            
                            progress = 10 + int((i + 1) / total_images * 50)
                            self.progress_update.emit("RESIZING", progress)
                else:
                    # For CBZ/CBR, images are file paths
                    image_tasks = [(img_path, temp_dir) for img_path in images]
                    
                    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
                        futures = [executor.submit(ImageProcessor.process_image, task) 
                                 for task in image_tasks]
                        
                        processed_images = []
                        for i, future in enumerate(futures):
                            if self.should_stop:
                                return
                            result = future.result()
                            if result:
                                processed_images.append(result)
                            
                            progress = 10 + int((i + 1) / len(futures) * 50)
                            self.progress_update.emit("RESIZING", progress)
                
                self.progress_update.emit("RESIZING", 60)
                self.progress_update.emit("COMPRESSING", 70)
                
                # Create new CBZ file
                self.progress_update.emit("REPACKAGING", 85)
                
                # Create temporary CBZ file first
                temp_cbz_path = file_path.parent / f"temp_{file_path.stem}.cbz"
                
                with zipfile.ZipFile(temp_cbz_path, 'w', zipfile.ZIP_DEFLATED) as cbz:
                    for img_path in sorted(processed_images):
                        if self.should_stop:
                            return
                        if os.path.exists(img_path):
                            arcname = os.path.basename(img_path)
                            cbz.write(img_path, arcname)
                
                self.progress_update.emit("REPACKAGING", 95)
                
                # Determine final file path
                if file_path.suffix.lower() != '.cbz':
                    # Convert PDF/CBR to CBZ - replace with .cbz extension
                    final_path = file_path.with_suffix('.cbz')
                else:
                    # Keep original CBZ path
                    final_path = file_path
                
                # Remove existing final file if it exists
                if final_path.exists():
                    os.remove(final_path)
                
                # Move temp file to final location
                os.rename(temp_cbz_path, final_path)
                
                # Remove original file if it was a different format
                if file_path.suffix.lower() != '.cbz' and file_path.exists():
                    os.remove(file_path)
                
                # Clean up backup file after successful processing
                if backup_path.exists():
                    os.remove(backup_path)
                
                self.progress_update.emit("REPACKAGING", 100)
                self.finished.emit(True, "Comic processed successfully!")
                
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")
    
    def process_pdf_image(self, pil_image, temp_dir, index):
        """Process a single PDF image"""
        try:
            processed_img = ImageProcessor.process_image(pil_image)
            if processed_img:
                output_path = os.path.join(temp_dir, f"page_{index:04d}.webp")
                processed_img.save(output_path, 'WEBP', quality=85, optimize=True)
                return output_path
        except Exception as e:
            print(f"Error processing PDF image {index}: {e}")
        return None
    
    def extract_from_pdf(self, pdf_path):
        """Extract images from PDF"""
        self.progress_update.emit("RESIZING", 5)
        try:
            images = pdf2image.convert_from_path(pdf_path, dpi=300)
            return images
        except Exception as e:
            print(f"Error extracting from PDF: {e}")
            return []
    
    def extract_from_cbz(self, cbz_path):
        """Extract images from CBZ"""
        self.progress_update.emit("RESIZING", 5)
        images = []
        try:
            with zipfile.ZipFile(cbz_path, 'r') as cbz:
                for filename in sorted(cbz.namelist()):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                        cbz.extract(filename, path=tempfile.gettempdir())
                        images.append(os.path.join(tempfile.gettempdir(), filename))
        except Exception as e:
            print(f"Error extracting from CBZ: {e}")
        return images
    
    def extract_from_cbr(self, cbr_path):
        """Extract images from CBR"""
        self.progress_update.emit("RESIZING", 5)
        images = []
        try:
            with rarfile.RarFile(cbr_path, 'r') as cbr:
                for filename in sorted(cbr.namelist()):
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')):
                        cbr.extract(filename, path=tempfile.gettempdir())
                        images.append(os.path.join(tempfile.gettempdir(), filename))
        except Exception as e:
            print(f"Error extracting from CBR: {e}")
        return images
    
    def stop(self):
        self.should_stop = True
    
    def is_already_crunched(self, file_path):
        """Check if file already contains WebP images"""
        try:
            if file_path.suffix.lower() == '.pdf':
                # PDFs are never pre-crunched
                return False
            elif file_path.suffix.lower() == '.cbz':
                # Check CBZ contents
                with zipfile.ZipFile(file_path, 'r') as cbz:
                    image_files = [f for f in cbz.namelist() 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'))]
                    if not image_files:
                        return False
                    # If more than 80% are WebP, consider it already crunched
                    webp_count = sum(1 for f in image_files if f.lower().endswith('.webp'))
                    return (webp_count / len(image_files)) > 0.8
            elif file_path.suffix.lower() == '.cbr':
                # Check CBR contents
                with rarfile.RarFile(file_path, 'r') as cbr:
                    image_files = [f for f in cbr.namelist() 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp'))]
                    if not image_files:
                        return False
                    # If more than 80% are WebP, consider it already crunched
                    webp_count = sum(1 for f in image_files if f.lower().endswith('.webp'))
                    return (webp_count / len(image_files)) > 0.8
            return False
        except Exception as e:
            print(f"Error checking if file is crunched: {e}")
            return False

class DragDropFrame(QFrame):
    """Custom frame for drag and drop functionality"""
    
    file_dropped = pyqtSignal(list)  # Changed to list for multiple files
    
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QFrame {
                background-color: #2b313a;
                border: 3px dashed #fc6467;
                border-radius: 10px;
            }
        """)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                # Accept if any URL is a valid file or directory
                for url in urls:
                    path = url.toLocalFile()
                    if os.path.isdir(path):
                        event.acceptProposedAction()
                        return
                    elif path.lower().endswith(('.pdf', '.cbz', '.cbr')):
                        event.acceptProposedAction()
                        return
        event.ignore()
    
    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            # Collect all valid files from URLs and directories
            file_paths = []
            for url in urls:
                path = url.toLocalFile()
                if os.path.isdir(path):
                    # Recursively find comic files in directory
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            if file_path.lower().endswith(('.pdf', '.cbz', '.cbr')):
                                file_paths.append(file_path)
                elif path.lower().endswith(('.pdf', '.cbz', '.cbr')):
                    file_paths.append(path)
            
            if file_paths:
                self.file_dropped.emit(file_paths)

class ComicCruncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.processor = None
        self.current_mode = "cruncher"  # "cruncher" or "combiner"
        
        self.init_ui()
        self.setup_fonts()
        
        # Initialize UI state
        self.update_title()
        self.update_progress_labels()
    
    def init_ui(self):
        self.setWindowTitle("Comic Cruncher")
        self.setFixedSize(1024, 1024)  # Back to original square size
        self.setStyleSheet(f"background-color: #363d46;")
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        
        # Title
        self.title_label = QLabel("COMIC CRUNCHER")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #ffd483; font-size: 72px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Compress • Optimize • Batch Process")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("color: #fc6467; font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.subtitle_label)
        
        # Mode toggle buttons
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(10)
        mode_layout.addStretch()
        
        self.cruncher_btn = QPushButton("COMIC CRUNCHER")
        self.cruncher_btn.setFixedSize(200, 40)
        self.cruncher_btn.clicked.connect(lambda: self.switch_mode("cruncher"))
        
        self.combiner_btn = QPushButton("COMIC COMBINER")
        self.combiner_btn.setFixedSize(200, 40)
        self.combiner_btn.clicked.connect(lambda: self.switch_mode("combiner"))
        
        self.update_mode_buttons()
        
        mode_layout.addWidget(self.cruncher_btn)
        mode_layout.addWidget(self.combiner_btn)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        
        # Left side - Drag and drop area
        self.drag_frame = DragDropFrame()
        self.drag_frame.setFixedSize(420, 480)
        self.drag_frame.file_dropped.connect(self.handle_file_drop)
        
        # Drag area layout
        drag_layout = QVBoxLayout(self.drag_frame)
        drag_layout.setContentsMargins(40, 40, 40, 40)
        drag_layout.setSpacing(30)
        
        # Drag text
        self.drag_text = QLabel()
        self.drag_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drag_text.setStyleSheet("color: #fc6467; font-size: 28px; font-weight: bold; line-height: 1.2; border: none; background: transparent;")
        drag_layout.addWidget(self.drag_text)
        
        # File types text
        self.types_text = QLabel()
        self.types_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.types_text.setStyleSheet("color: #fc6467; font-size: 24px; font-weight: bold; margin-top: 20px; border: none; background: transparent;")
        drag_layout.addWidget(self.types_text)
        
        # Compression details
        self.details_text = QLabel()
        self.details_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_text.setStyleSheet("color: #fc6467; font-size: 24px; font-weight: bold; margin-top: 20px; border: none; background: transparent;")
        drag_layout.addWidget(self.details_text)
        
        # Update text based on current mode
        self.update_drag_area_text()
        
        content_layout.addWidget(self.drag_frame)
        
        # Right side - File info area
        info_frame = QFrame()
        info_frame.setFixedSize(420, 480)
        info_frame.setStyleSheet("background-color: #282c32; border-radius: 10px;")
        
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(10)
        
        # Activity feed title
        feed_title = QLabel("ACTIVITY FEED")
        feed_title.setStyleSheet("color: #ffd483; font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        info_layout.addWidget(feed_title)
        
        # Activity feed area (scrollable but no visible scrollbar)
        self.activity_feed = QTextEdit()
        self.activity_feed.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #ffd483;
                font-size: 14px;
                font-weight: bold;
                padding: 0px;
            }
            QScrollBar:vertical {
                width: 0px;
                background: transparent;
            }
        """)
        self.activity_feed.setReadOnly(True)
        self.activity_feed.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.activity_feed.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.activity_feed.setText("Drop files to begin...")
        info_layout.addWidget(self.activity_feed)
        content_layout.addWidget(info_frame)
        layout.addLayout(content_layout)
        
        # Progress bars section
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(15)
        
        # Progress labels and bars
        self.progress_bars = {}
        self.stage_labels = {}  # Store references to stage labels
        stages = ["RESIZING", "COMPRESSING", "REPACKAGING"]
        
        for stage in stages:
            stage_layout = QHBoxLayout()
            stage_layout.setSpacing(20)
            
            # Label
            label = QLabel(stage)
            label.setFixedWidth(200)
            label.setStyleSheet("color: #ffd483; font-size: 24px; font-weight: bold;")
            stage_layout.addWidget(label)
            self.stage_labels[stage] = label  # Store reference to the label
            
            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setFixedHeight(20)  # Made thinner
            progress_bar.setStyleSheet("""
                QProgressBar {
                    border: none;
                    border-radius: 10px;
                    background-color: #2b313a;
                    text-align: center;
                    color: #ffd483;
                    font-weight: bold;
                    font-size: 14px;
                }
                QProgressBar::chunk {
                    border-radius: 10px;
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #fc6467, stop:1 #ffd483);
                }
            """)
            progress_bar.setValue(0)
            stage_layout.addWidget(progress_bar)
            
            # Percentage label
            percent_label = QLabel("0%")
            percent_label.setFixedWidth(50)
            percent_label.setStyleSheet("color: #fc6467; font-size: 18px; font-weight: bold;")
            stage_layout.addWidget(percent_label)
            
            self.progress_bars[stage] = (progress_bar, percent_label)
            progress_layout.addLayout(stage_layout)
        
        layout.addLayout(progress_layout)
    
    def setup_fonts(self):
        """Load Google Fonts"""
        # For now, using system fonts that are similar
        # In production, you'd download and load the actual Google Fonts
        title_font = QFont("Arial Black", 72, QFont.Weight.Bold)
        title_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2)
        self.title_label.setFont(title_font)
    
    def switch_mode(self, mode):
        """Switch between cruncher and combiner modes"""
        if self.processor and self.processor.isRunning():
            return  # Don't switch while processing
            
        self.current_mode = mode
        self.update_mode_buttons()
        self.update_drag_area_text()
        self.update_progress_labels()
        self.update_title()  # Add this line
        self.clear_feed()
    
    def update_title(self):
        """Update main title based on current mode"""
        if self.current_mode == "cruncher":
            self.title_label.setText("COMIC CRUNCHER")
        else:
            self.title_label.setText("COMIC COMBINER")
    
    def update_mode_buttons(self):
        """Update button styles based on current mode"""
        active_style = """
            QPushButton {
                background-color: #ffd483;
                color: #363d46;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
        """
        
        inactive_style = """
            QPushButton {
                background-color: #2b313a;
                color: #ffd483;
                border: 2px solid #ffd483;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #363d46;
            }
        """
        
        if self.current_mode == "cruncher":
            self.cruncher_btn.setStyleSheet(active_style)
            self.combiner_btn.setStyleSheet(inactive_style)
        else:
            self.cruncher_btn.setStyleSheet(inactive_style)
            self.combiner_btn.setStyleSheet(active_style)
    
    def update_drag_area_text(self):
        """Update drag area text based on current mode"""
        if self.current_mode == "cruncher":
            self.drag_text.setText("DRAG YOUR COMIC\nFILES OR FOLDER HERE.")
            self.types_text.setText("ACCEPTING .PDFS,\n.CBZS, & .CBRS.")
            self.details_text.setText("COMPRESSES TO\n2500 X 2500\n(RETAINING RATIO\nAND .WEBP -85%.")
            self.subtitle_label.setText("Compress • Optimize • Batch Process")
        else:
            self.drag_text.setText("DRAG COMIC ISSUES\nTO COMBINE HERE.")
            self.types_text.setText("ACCEPTING SEQUENTIAL\n.CBZS & .CBRS.")
            self.details_text.setText("COMBINES INTO TPB\nREMOVES ORIGINALS\nAUTO-NAMES COLLECTION")
            self.subtitle_label.setText("Combine • Organize • Collection")
    
    def update_progress_labels(self):
        """Update progress bar labels based on current mode"""
        if self.current_mode == "cruncher":
            stages = ["RESIZING", "COMPRESSING", "REPACKAGING"]
        else:
            stages = ["SCANNING", "COMBINING", "FINALIZING"]
        
        # Update the actual progress bar labels
        original_stages = ["RESIZING", "COMPRESSING", "REPACKAGING"]
        for i, new_label in enumerate(stages):
            if i < len(original_stages):
                original_stage = original_stages[i]
                if original_stage in self.stage_labels:
                    self.stage_labels[original_stage].setText(new_label)
        
        # Store the current stage mapping for progress updates
        self.current_stages = stages
    
    def add_to_feed(self, message, is_current=False):
        """Add a message to the activity feed"""
        if is_current:
            # Current item in yellow
            color_message = f'<span style="color: #ffd483;">🔄 {message}</span>'
        else:
            # Completed items in red
            color_message = f'<span style="color: #fc6467;">✓ {message}</span>'
        
        current_text = self.activity_feed.toHtml()
        if "Drop files to begin..." in current_text:
            # First message, replace placeholder
            self.activity_feed.setHtml(color_message)
        else:
            # Append new message
            self.activity_feed.append(color_message)
        
        # Auto-scroll to bottom - fixed for PyQt6
        cursor = self.activity_feed.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.activity_feed.setTextCursor(cursor)
    
    def clear_feed(self):
        """Clear the activity feed"""
        self.activity_feed.setText("Drop files to begin...")
    
    def handle_file_drop(self, file_paths):
        """Handle dropped files (single or multiple)"""
        if self.processor and self.processor.isRunning():
            return  # Already processing
        
        # Reset progress bars
        for stage, (bar, label) in self.progress_bars.items():
            bar.setValue(0)
            label.setText("0%")
        
        if self.current_mode == "cruncher":
            # Comic Cruncher mode
            if len(file_paths) == 1:
                # Single file processing
                self.processor = ComicProcessor(file_paths[0])
                self.processor.progress_update.connect(self.update_progress)
                self.processor.file_info_update.connect(self.update_file_info)
                self.processor.finished.connect(self.processing_finished)
                self.processor.start()
            else:
                # Batch processing
                self.processor = BatchProcessor(file_paths)
                self.processor.progress_update.connect(self.update_progress)
                self.processor.file_info_update.connect(self.update_file_info)
                self.processor.batch_progress.connect(self.update_batch_progress)
                self.processor.finished.connect(self.processing_finished)
                self.processor.start()
        else:
            # Comic Combiner mode
            # Filter to only CBZ/CBR files
            comic_files = [f for f in file_paths if f.lower().endswith(('.cbz', '.cbr'))]
            
            if len(comic_files) < 2:
                self.add_to_feed("Error: Need at least 2 comic files to combine", is_current=False)
                return
            
            self.processor = ComicCombiner(comic_files)
            self.processor.progress_update.connect(self.update_progress)
            self.processor.file_info_update.connect(self.update_file_info)
            self.processor.finished.connect(self.processing_finished)
            self.processor.start()
    
    def update_progress(self, stage, percentage):
        """Update progress bar for specific stage"""
        print(f"Progress update: {stage} {percentage}%")  # Debug print
        
        # Map stage to current mode if needed
        if hasattr(self, 'current_stages'):
            stage_list = list(self.progress_bars.keys())
            mode_stages = self.current_stages
            
            # Find which progress bar to update based on stage
            if stage in mode_stages:
                stage_index = mode_stages.index(stage)
                if stage_index < len(stage_list):
                    actual_stage = stage_list[stage_index]
                    if actual_stage in self.progress_bars:
                        bar, label = self.progress_bars[actual_stage]
                        bar.setValue(percentage)
                        label.setText(f"{percentage}%")
                        print(f"Updated {actual_stage} bar to {percentage}%")  # Debug
                        return
        
        # Fallback: try direct stage match
        if stage in self.progress_bars:
            bar, label = self.progress_bars[stage]
            bar.setValue(percentage)
            label.setText(f"{percentage}%")
            print(f"Direct update {stage} to {percentage}%")  # Debug
    
    def update_batch_progress(self, current, total):
        """Update batch progress display"""
        batch_percentage = int((current / total) * 100)
        # Update the first progress bar to show batch progress
        bar, label = self.progress_bars["RESIZING"]
        bar.setValue(batch_percentage)
        label.setText(f"{current}/{total}")
    
    def update_file_info(self, file_path):
        """Update file info display"""
        if isinstance(file_path, str):
            if "Starting batch:" in file_path:
                # Batch start info
                self.add_to_feed(file_path, is_current=True)
            elif "Processing:" in file_path:
                # Currently processing file
                self.add_to_feed(file_path, is_current=True)
            elif "Completed:" in file_path or "Skipped:" in file_path or "Error:" in file_path:
                # File completed
                self.add_to_feed(file_path, is_current=False)
            else:
                # Other batch info
                self.add_to_feed(file_path, is_current=True)
        else:
            # Single file info
            path_obj = Path(file_path)
            message = f"Processing: {path_obj.name}"
            self.add_to_feed(message, is_current=True)
    
    def processing_finished(self, success, message):
        """Handle processing completion"""
        if success:
            if "already crunched" in message.lower():
                # Special handling for already crunched files
                self.add_to_feed(f"Skipped: {message}", is_current=False)
                QTimer.singleShot(3000, self.reset_ui)
            else:
                # Normal completion
                self.add_to_feed(f"Completed: {message}", is_current=False)
                # Complete all progress bars
                for stage in ["RESIZING", "COMPRESSING", "REPACKAGING", "SCANNING", "COMBINING", "FINALIZING"]:
                    if stage in self.progress_bars:
                        bar, label = self.progress_bars[stage]
                        bar.setValue(100)
                        label.setText("100%")
                
                # Reset after delay
                QTimer.singleShot(3000, self.reset_ui)
        else:
            self.add_to_feed(f"Error: {message}", is_current=False)
            QTimer.singleShot(5000, self.reset_ui)
    
    def reset_ui(self):
        """Reset UI to initial state"""
        # Reset all progress bars
        for stage, (bar, label) in self.progress_bars.items():
            bar.setValue(0)
            label.setText("0%")
        
        # Don't clear the feed - keep the history of completed files

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Comic Cruncher")
    app.setApplicationVersion("1.0")
    
    window = ComicCruncher()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
