# 📚 Comic Cruncher - Complete Usage Guide

## Overview

Comic Cruncher is a professional comic processing tool that helps you compress, convert, and organize your digital comic collection. This guide covers everything from basic usage to advanced features.

---

## 🚀 Quick Start

### Free Version Setup

1. **Download and Install**
   ```bash
   # Clone repository
   git clone https://github.com/wesellis/comic-cruncher.git
   cd comic-cruncher
   
   # Install dependencies (Windows)
   install.bat
   
   # Or manually
   pip install -r requirements.txt
   ```

2. **Install Required Tools**
   - **Poppler** (for PDF support): [Download here](https://github.com/oschwartz10612/poppler-windows/releases/)
   - **WinRAR/7-Zip** (for CBR support)

3. **Launch Application**
   ```bash
   # Windows
   run.bat
   
   # Or directly
   python comic_cruncher.py
   ```

### Pro Version Activation

1. **Purchase License**
   - Buy from [Gumroad](https://gumroad.com/l/comic-cruncher-pro)
   - You'll receive a license key via email

2. **Activate Pro Features**
   - Launch Comic Cruncher
   - Click "Activate Pro" button
   - Enter your license key
   - Restart application

---

## 📖 Basic Usage

### Comic Cruncher Mode (Compression)

1. **Select Mode**
   - Ensure "COMIC CRUNCHER" is selected (default)

2. **Add Comics**
   - Drag and drop files into the drop zone
   - Or click to browse and select files
   - Supports: PDF, CBZ, CBR formats

3. **Processing**
   - Files are automatically queued
   - Progress shown for each stage:
     - Extracting
     - Processing
     - Compressing
     - Finalizing

4. **Results**
   - Processed files saved in same directory
   - Original files backed up as `.backup`
   - Activity feed shows compression ratios

### Comic Combiner Mode (TPB Creation)

**Note: Pro feature only**

1. **Switch to Combiner Mode**
   - Click "COMIC COMBINER" toggle

2. **Add Sequential Issues**
   - Drag complete series or story arcs
   - Files must have issue numbers
   - Supported patterns:
     - `Series Name 001.cbz`
     - `Series Name #1.cbr`
     - `Series Name Issue 1.cbz`

3. **Automatic Processing**
   - Auto-detects series and issue numbers
   - Groups every 12 issues into volumes
   - Creates files like: `Series Name Vol 1 (Issues 1-12).cbz`

4. **Cleanup**
   - Original individual issues moved to `_processed` folder
   - Combined TPBs in main directory

---

## 🎯 Advanced Features

### Batch Processing

**Free Version**: Limited to 10 comics per day
**Pro Version**: Unlimited batch processing

1. **Folder Processing**
   ```
   - Drag entire folder
   - Recursively finds all comics
   - Maintains folder structure
   ```

2. **Queue Management**
   - View all queued items
   - Cancel individual items
   - Pause/resume processing

### Custom Compression Settings

**Pro Feature**

1. **Access Settings**
   - File → Preferences → Compression

2. **Adjust Parameters**
   ```python
   # Quality (1-100, default: 85)
   compression_quality = 85
   
   # Max dimensions (default: 2500x2500)
   max_width = 2500
   max_height = 2500
   
   # Format (WebP recommended)
   output_format = "webp"
   ```

3. **Profiles**
   - **Storage Saver**: 70% quality, 2000px max
   - **Balanced**: 85% quality, 2500px max (default)
   - **Archive**: 95% quality, 3000px max
   - **Custom**: Define your own

### Command Line Interface

**Pro Feature**

```bash
# Process single file
python comic_cruncher.py --file "comic.cbr" --quality 85

# Batch process folder
python comic_cruncher.py --folder "C:\Comics" --recursive

# Combine series
python comic_cruncher.py --combine --series "Batman" --input "C:\Batman"

# Custom output
python comic_cruncher.py --file "comic.pdf" --output "C:\Processed"
```

### API Access

**Pro Feature**

```python
from comic_cruncher_api import ComicProcessor

# Initialize with license
processor = ComicProcessor(license_key="YOUR_KEY")

# Process single file
result = processor.compress(
    input_file="comic.cbr",
    quality=85,
    max_size=(2500, 2500)
)

# Batch process
results = processor.batch_compress(
    folder="C:\Comics",
    recursive=True
)

# Combine series
tpb = processor.combine_series(
    series_name="Saga",
    input_folder="C:\Saga",
    issues_per_volume=12
)
```

---

## 🔧 Optimization Tips

### Performance

1. **Multi-Core Usage**
   - Automatically uses all CPU cores
   - Close other applications for best performance
   - SSD recommended for temp files

2. **Memory Management**
   - 8GB+ RAM recommended for large batches
   - Process in smaller batches if low on memory

3. **Storage**
   - Ensure 2x space of comics being processed
   - Temp files cleaned automatically
   - Use external drive for large libraries

### Quality vs Size

1. **Finding Balance**
   - 85% quality = best size/quality ratio
   - 70% quality = maximum compression
   - 95% quality = archival quality

2. **Resolution Guidelines**
   - 2500px = standard tablets/readers
   - 3000px = high-res tablets
   - 2000px = phones/small devices

### File Organization

1. **Naming Conventions**
   ```
   Good:
   ✅ Saga 001.cbz
   ✅ Saga 002.cbz
   ✅ The Walking Dead 001.cbz
   
   Bad:
   ❌ Saga1.cbz (needs padding)
   ❌ Saga - First Issue.cbz (no number)
   ❌ Comic.cbz (no series name)
   ```

2. **Folder Structure**
   ```
   Comics/
   ├── Marvel/
   │   ├── Spider-Man/
   │   └── X-Men/
   ├── DC/
   │   ├── Batman/
   │   └── Superman/
   └── Image/
       ├── Saga/
       └── Walking Dead/
   ```

---

## 🛠️ Troubleshooting

### Common Issues

**"Reached daily limit"**
- Free version limited to 10 comics/day
- Resets at midnight local time
- Upgrade to Pro for unlimited

**"Cannot process CBR files"**
- Install WinRAR or 7-Zip
- Ensure RAR support in PATH
- Try converting to CBZ first

**"Memory error on large files"**
- Process files individually
- Reduce quality setting
- Close other applications
- Add more RAM

**"Combiner not detecting series"**
- Check file naming (needs numbers)
- Ensure consistent naming
- Remove special characters
- Use rename tool first

### Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| E001 | Invalid license | Re-enter license key |
| E002 | Corrupt file | Try different file |
| E003 | No space | Free up disk space |
| E004 | Missing dependency | Run install.bat |
| E005 | Format unsupported | Convert to CBZ first |

---

## 📊 Best Practices

### For Publishers

1. **Standardize Output**
   - Set consistent quality profiles
   - Use standard dimensions
   - Maintain metadata

2. **Automation**
   - Use CLI for batch processing
   - Schedule regular compressions
   - Integrate with workflows

### For Collectors

1. **Preserve Originals**
   - Keep uncompressed backups
   - Use archive quality for rare comics
   - Organize by publisher/series

2. **Space Management**
   - Process largest files first
   - Use storage saver profile
   - Regular cleanup of backups

### For Libraries

1. **Bulk Processing**
   - Process by collection
   - Maintain folder structure
   - Generate processing reports

2. **Quality Control**
   - Spot-check processed files
   - Maintain quality standards
   - Document settings used

---

## 🔐 Security & Privacy

### Data Handling

- **Local Processing**: All processing done locally
- **No Upload**: Comics never leave your computer
- **No Tracking**: No usage analytics collected
- **License Check**: Only license validation uses internet

### Backup Safety

- **Auto-backup**: Original files preserved
- **Non-destructive**: Never modifies originals
- **Recovery**: Easy restore from .backup files

---

## 📞 Support

### Free Version
- GitHub Issues: [Report bugs](https://github.com/wesellis/comic-cruncher/issues)
- Community Forum: [Discussions](https://github.com/wesellis/comic-cruncher/discussions)
- FAQ: Check website

### Pro Version
- Email: support@comiccruncher.com
- Response Time: Within 24 hours
- Include: License key, error logs
- Priority: Bug fixes and feature requests

---

## 🚀 Advanced Workflows

### Automated Library Processing

```python
# Weekly compression script
import os
from comic_cruncher_api import ComicProcessor

processor = ComicProcessor(license_key="YOUR_KEY")

# Find new comics
new_comics = processor.find_unprocessed("C:\\Comics")

# Process with logging
for comic in new_comics:
    result = processor.compress(comic)
    print(f"Processed: {comic} - Saved: {result.space_saved}MB")
```

### Integration Examples

1. **NAS Integration**
   - Mount network drives
   - Process to local, copy back
   - Maintain library structure

2. **Cloud Backup**
   - Process locally first
   - Upload compressed versions
   - Keep originals offline

3. **Reading Apps**
   - Optimize for device specs
   - Sync processed files
   - Maintain reading progress

---

*Last Updated: June 2025*
*Version: 2.0*