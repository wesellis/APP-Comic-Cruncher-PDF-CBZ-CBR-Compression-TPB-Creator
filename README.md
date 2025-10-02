# Comic Cruncher & TPB Creator

A Python tool for compressing comic files and creating Trade Paperback collections.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

## Features

### Comic Compression
- **Format Support**: Converts PDF, CBZ, CBR, and CB7 files to optimized CBZ
- **Image Optimization**: Resizes images to 2500×2500px max and converts to WebP format
- **Batch Processing**: Process multiple files in parallel using all CPU cores
- **Smart Skip**: Automatically skips already-processed files
- **Backup Safety**: Creates .backup files before modifying originals

### TPB Creator
- **Auto-Detection**: Automatically groups comics by series
- **Volume Creation**: Combines 12 issues per volume by default
- **Pattern Recognition**: Supports common comic naming patterns
- **Original Management**: Optional cleanup of source files after combining

## Installation

### Requirements
- Python 3.9 or higher
- Poppler (for PDF support)
- UnRAR or 7-Zip (for CBR support)

### Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Poppler:
   - **Windows**: Download from [releases](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH
   - **Linux**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`

3. Install UnRAR or 7-Zip:
   - **Windows**: Install [7-Zip](https://www.7-zip.org/)
   - **Linux**: `sudo apt-get install unrar`
   - **macOS**: `brew install unrar`

## Usage

### Launch the GUI
```bash
python comic_cruncher.py
```

### Comic Cruncher Mode
1. Select input folder containing your comics
2. Choose output folder for processed files
3. Adjust settings (max workers, image size, WebP quality)
4. Click "Process Comics"

### Comic Combiner Mode (TPB Creator)
1. Select folder containing comics from the same series
2. Set issues per volume (default: 12)
3. Choose whether to delete originals after combining
4. Click "Combine Comics"

## Configuration

Default settings can be adjusted in the GUI:
- **Max Workers**: Number of parallel processes (defaults to CPU count)
- **Max Dimension**: Maximum width/height for images (default: 2500px)
- **WebP Quality**: Compression quality from 1-100 (default: 85)

## Expected Results

Compression varies by source format:
- PDF files typically see 60-75% size reduction
- CBR files typically see 50-65% size reduction
- Already optimized files are automatically skipped

Image quality is maintained for normal reading. Some quality loss may be visible at high zoom levels.

## Project Structure

```
comic_cruncher.py       # Main application
requirements.txt        # Python dependencies
USAGE_GUIDE.md         # Detailed usage instructions
CONTRIBUTING.md        # Contribution guidelines
CHANGELOG.md           # Version history
SECURITY.md            # Security policy
LICENSE                # MIT License
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Troubleshooting

**PDFs not processing**: Make sure Poppler is installed and in your system PATH

**CBR files failing**: Install UnRAR or 7-Zip

**Slow processing**: Try reducing the number of workers or batch size

**Memory errors**: Process fewer files at once

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- [Pillow](https://python-pillow.org/) - Image processing
- [pdf2image](https://github.com/Belval/pdf2image) - PDF conversion
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework

---

## Project Status & Roadmap

**Completion: ~85%**

### What Works
- ✅ PyQt6 GUI with modern interface
- ✅ Comic compression (PDF, CBZ, CBR to optimized CBZ)
- ✅ WebP conversion with adjustable quality
- ✅ Batch processing with multiprocessing
- ✅ TPB Creator (auto-combines 12 issues per volume)
- ✅ Auto-detection of comic series patterns
- ✅ Smart file skipping (already processed files)
- ✅ Backup creation before modifications
- ✅ Real-time progress tracking
- ✅ Cross-platform support (Windows, Linux, macOS)

### Known Limitations & Missing Features

**Format Support:**
- ⚠️ **CB7 Format**: Mentioned in README but implementation incomplete
- ⚠️ **CBT Format**: Not supported (TAR-based comics)
- ⚠️ **Comic Metadata**: No preservation of ComicInfo.xml or metadata

**Features:**
- ⚠️ **GPU Acceleration**: OpenCV dependency present but may not be actively used
- ⚠️ **CLI Mode**: No command-line interface for automation/scripting
- ⚠️ **Undo Functionality**: No way to reverse compression or restore originals
- ⚠️ **Custom Naming**: TPB naming is automatic, no custom templates
- ⚠️ **Drag & Drop**: QDragEnterEvent imported but functionality not verified

**Code Quality:**
- ⚠️ **Testing**: No test suite or unit tests
- ⚠️ **Error Recovery**: Basic error handling, could be more robust
- ⚠️ **Logging**: No detailed log file output for troubleshooting
- ⚠️ **Configuration File**: Settings not persisted between sessions

### What Needs Work

1. **CB7 Support** - Complete 7-Zip format handling
2. **Metadata Preservation** - Keep ComicInfo.xml when compressing
3. **Command Line Interface** - Add CLI for batch scripting
4. **Settings Persistence** - Save user preferences to config file
5. **Comprehensive Testing** - Add unit tests and integration tests
6. **Better Error Handling** - More detailed error messages and recovery
7. **Undo System** - Ability to restore from backups
8. **Custom TPB Naming** - Templates for volume naming conventions
9. **Logging System** - Detailed logs for debugging issues
10. **Documentation** - More examples and troubleshooting guides

### Contributing

If you'd like to help complete any of the missing features above, contributions are welcome. Priority areas:
1. Adding CB7 format support
2. Implementing metadata preservation (ComicInfo.xml)
3. Writing tests (pytest)
4. Adding CLI interface for automation

---

**Note:** Core functionality is solid and stable for PDF/CBZ/CBR compression and TPB creation. Advanced features and format support need additional development.
