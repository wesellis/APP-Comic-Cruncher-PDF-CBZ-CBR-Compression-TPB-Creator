# Comic Cruncher & Combiner

A powerful dual-mode comic processing application with parallel processing and modern UI. Features both comic compression/optimization and TPB (Trade Paperback) collection creation capabilities.

## 🚀 Features

### Comic Cruncher Mode
- **Universal format support**: PDF, CBZ, CBR → optimized CBZ
- **Parallel processing**: Uses all CPU cores for maximum speed
- **Smart resizing**: Max 2500×2500 while maintaining aspect ratio
- **WebP compression**: 85% quality for optimal size/quality balance
- **Batch processing**: Handle multiple files simultaneously
- **Smart skip detection**: Avoids re-processing already optimized files
- **Safe backup system**: Creates .backup files before processing

### Comic Combiner Mode (NEW!)
- **Auto-detection**: Intelligently identifies comic series patterns
- **TPB creation**: Combines issues into Trade Paperback collections
- **Smart batching**: Groups every 12 issues into separate volumes
- **Pattern recognition**: Supports multiple naming conventions
- **Auto-naming**: Generates proper "Series Vol X (Issues 1-12)" format
- **Original cleanup**: Removes individual issues after combining

### Interface
- **Modern GUI**: Sleek drag-and-drop interface with real-time progress
- **Dual-mode toggle**: Switch between Cruncher and Combiner modes
- **Activity feed**: Live processing updates and batch summaries
- **Visual progress**: Stage-by-stage progress indicators
- **File size reporting**: Shows compression ratios and space saved

## 📋 System Requirements

- **Python**: 3.8+ (3.9+ recommended)
- **RAM**: 4GB+ (8GB+ for large batches)
- **CPU**: Multi-core recommended for parallel processing
- **Storage**: Adequate space for temporary files during processing

## 🛠️ Installation

### Quick Start (Windows)
1. **Download** the project files
2. **Run install.bat** as administrator - handles all dependencies
3. **Install Poppler** for PDF support (guided in installer)
4. **Launch** with run.bat or `python comic_cruncher.py`

### Manual Installation
1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Poppler (for PDF support):**
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/)
     - Extract and add `bin` folder to system PATH
   - **Linux**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`

3. **Install RAR support (for CBR files):**
   - **Windows**: Install WinRAR or 7-Zip
   - **Linux**: `sudo apt-get install unrar`
   - **macOS**: `brew install unrar`

## 🎯 Usage

### Comic Cruncher Mode
1. **Launch** the application
2. **Select "COMIC CRUNCHER"** mode (default)
3. **Drag and drop** PDF, CBZ, or CBR files (single file or batch)
4. **Watch progress** as files are optimized with parallel processing
5. **Review results** in the activity feed

### Comic Combiner Mode
1. **Switch to "COMIC COMBINER"** mode
2. **Drag and drop** sequential comic issues (CBZ/CBR format)
3. **Auto-detection** identifies series and issue numbers
4. **Combination** creates TPB volumes (12 issues each)
5. **Cleanup** removes original individual issues

## 📁 File Structure

```
comic_cruncher.py      # Main application with both modes
requirements.txt       # Python dependencies
install.bat           # Windows automated installer
run.bat              # Windows launcher with error checking
fix_dependencies.bat  # Troubleshooting utility
README.md            # This documentation
.gitignore           # Git ignore file
```

## 🔧 Technical Details

### Compression Engine
- **Parallel image processing**: Utilizes ProcessPoolExecutor for CPU-intensive tasks
- **Memory optimization**: Batched processing prevents memory overflow
- **Format standardization**: All outputs use CBZ (ZIP) format
- **Quality preservation**: Smart resizing maintains visual quality
- **WebP conversion**: Modern format with superior compression

### Comic Combiner Logic
- **Pattern detection**: Multiple regex patterns for issue identification
  - `Series Name 001` (zero-padded)
  - `Series Name Issue 1`
  - `Series Name #1`
  - `Series Name 1` (fallback)
- **Intelligent sorting**: Natural ordering by issue number
- **Volume management**: 12-issue batches with proper naming
- **Range formatting**: Smart issue range strings (e.g., "1-12", "14, 16-20")

### Supported Naming Patterns
```
✅ Saga 001.cbz
✅ Saga Issue 1.cbr
✅ Saga #1.cbz
✅ The Walking Dead 001.cbz
✅ Batman Issue 675.cbr
✅ X-Men #1.cbz
```

## 🔍 Troubleshooting

### Common Issues

**"No module named 'pdf2image'"**
- Install Poppler as described above
- Ensure Poppler's `bin` folder is in system PATH
- Restart command prompt after PATH changes
- Test with: `pdftoppm -h` (should show help)

**"Cannot extract CBR files"**
- **Windows**: Install WinRAR or 7-Zip
- **Linux**: `sudo apt-get install unrar`
- **macOS**: `brew install unar` (note: unar, not unrar)

**Slow processing**
- App automatically uses all CPU cores
- Large files require more processing time
- Ensure adequate RAM for batch operations
- Close other applications during processing

**Combiner not detecting series**
- Check file naming follows supported patterns
- Ensure issue numbers are present and numerical
- Use consistent naming across all issues
- Remove special characters from filenames

**GUI won't start**
- Ensure all dependencies installed: `pip install -r requirements.txt`
- On Linux: Install GUI dependencies: `sudo apt-get install libxcb-xinerama0 libgl1-mesa-glx`
- Try running in terminal to see error messages

### Quick Fixes
- **Windows**: Run `fix_dependencies.bat` to resolve package conflicts
- **All platforms**: Check `install.bat` output for failed installations
- Verify Python 3.8+ is installed and in PATH
- Update pip: `python -m pip install --upgrade pip`

## 🎨 Interface Overview

### Main Elements
- **Mode Toggle**: Switch between Cruncher and Combiner
- **Drag Area**: Visual drop zone for files/folders
- **Activity Feed**: Real-time processing updates
- **Progress Bars**: Stage-by-stage completion indicators
- **Dynamic Labels**: Mode-specific progress descriptions

### Activity Feed Messages
- **🔄 Current**: Items being processed (yellow)
- **✓ Completed**: Finished items (red)
- **File sizes**: Compression ratios shown
- **Batch summaries**: Final statistics

## 📊 Performance

### Benchmarks (typical results)
- **Single file**: 30-60 seconds depending on size
- **Batch processing**: Parallel execution scales with CPU cores
- **Compression ratios**: 40-70% size reduction typical
- **Memory usage**: ~2-4GB for large batches

### Optimization Tips
- **Close other applications** during large batch processing
- **Use SSD storage** for faster temporary file operations
- **Ensure adequate RAM** for the number of files being processed

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional comic format support
- Enhanced pattern recognition
- UI/UX improvements
- Performance optimizations
- Cross-platform compatibility

## 📄 License

MIT License - Feel free to use, modify, and distribute!

## 🔗 Links

- **Poppler Downloads**: [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases/)
- **Python Downloads**: [python.org](https://python.org)
- **WinRAR**: [win-rar.com](https://win-rar.com)

---

**Version**: 2.0  
**Last Updated**: June 2025  
**Compatibility**: Windows 10/11, Linux, macOS