# Comic Cruncher

A fast, parallel-processing comic compression tool with a sleek UI. Converts PDF, CBZ, and CBR files to optimized CBZ format.

## Features

- **Universal comic format support**: PDF, CBZ, CBR
- **Parallel processing**: Uses all CPU cores for maximum speed
- **Smart resizing**: Max 2500x2500 while maintaining aspect ratio
- **WebP compression**: 85% quality for optimal size/quality balance
- **Safe backup system**: Creates .backup files before processing
- **Modern UI**: Drag-and-drop interface with real-time progress

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Poppler (for PDF support):**
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Extract and add the `bin` folder to your system PATH
   - **Linux**: `sudo apt-get install poppler-utils`
   - **macOS**: `brew install poppler`

## Usage

1. **Run the application:**
   ```bash
   python comic_cruncher.py
   ```

2. **Drag and drop** a PDF, CBZ, or CBR file onto the interface

3. **Watch the progress** as your comic is processed with parallel compression

4. **Your original file is safely backed up** (with .backup extension) and replaced with the optimized CBZ

## Technical Details

- **Image processing**: Parallel conversion using all CPU cores
- **Aspect ratio preservation**: Smart resizing algorithm
- **Format conversion**: Everything becomes CBZ (ZIP-based comic format)
- **WebP optimization**: 85% quality with size optimization enabled
- **Memory efficient**: Processes images in batches to avoid memory issues

## File Structure

```
comic_cruncher.py    # Main application
requirements.txt     # Python dependencies
README.md           # This file
```

## System Requirements

- Python 3.8+
- 4GB+ RAM recommended for large comics
- Multi-core CPU for best performance

## Troubleshooting

**"No module named 'pdf2image'"**
- Install Poppler as described above

**"Cannot extract CBR files"**
- Ensure WinRAR or 7-Zip is installed on Windows

**Slow processing**
- The app uses all CPU cores automatically - larger files simply take more time

## License

MIT License - Feel free to use and modify!
