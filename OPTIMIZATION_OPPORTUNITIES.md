# OPTIMIZATION NOTES FOR COMIC CRUNCHER

## CRITICAL ISSUES TO FIX:

### 1. MEMORY LEAK (Lines 413, 459, 626, 647)
```python
# CURRENT (BAD):
cbz.extract(filename, path=tempfile.gettempdir())
images.append(os.path.join(tempfile.gettempdir(), filename))
# Never cleaned up!

# OPTIMIZED:
with tempfile.TemporaryDirectory() as temp_dir:
    cbz.extract(filename, path=temp_dir)
    images.append(os.path.join(temp_dir, filename))
    # Auto-cleanup when context exits
```

### 2. DUPLICATE CODE (400+ lines repeated)
```python
# CREATE SHARED UTILITY CLASS:
class ComicExtractor:
    @staticmethod
    def extract_images(file_path, temp_dir=None):
        """Single method to extract from any format"""
        # Unified extraction logic
        
    @staticmethod
    def process_batch(file_list, progress_callback=None):
        """Shared batch processing"""
```

### 3. INEFFICIENT MEMORY USAGE
```python
# CURRENT: Extract to disk, then read
cbz.extract(filename, path=temp_dir)
with Image.open(disk_path) as img:

# OPTIMIZED: Process in memory
with cbz.open(filename) as file_data:
    img = Image.open(io.BytesIO(file_data.read()))
```

### 4. MISSING OPTIMIZATION FLAGS
```python
# ADD THESE OPTIMIZATIONS:
- ZIP_STORED for already compressed WebP files
- Parallel extraction + processing pipeline
- Smart memory management based on file size
- Progressive loading for large files
```

## ESTIMATED IMPACT:
- 40-60% faster processing
- 70% less memory usage  
- Zero temp file accumulation
- Better error reporting
- Smoother progress updates

## TIME TO IMPLEMENT: 2-3 hours