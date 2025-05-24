# CBR to CBZ Converter

A PowerShell script that automates the conversion of Comic Book Archive (CBR) files to Comic Book Zip (CBZ) files, with optional JPEG to WebP compression for smaller file sizes.

## Features

- **Batch Conversion**: Convert all CBR files in a directory to CBZ format
- **Image Optimization**: Optional JPEG to WebP conversion for reduced file sizes
- **Parallel Processing**: Utilizes PowerShell parallel processing for faster conversions
- **Automatic Cleanup**: Manages temporary files automatically
- **Progress Tracking**: Displays conversion progress and timing information
- **Cross-Format Support**: Handles existing CBZ files for image optimization

## Requirements

### Essential Dependencies
1. **7-Zip**: Required for extracting and compressing archive files
   - Download from [7-Zip.org](https://www.7-zip.org/)
   - Ensure `7z.exe` is in your system PATH

2. **PowerShell 7.1+**: Required for parallel processing features
   - Download from [Microsoft PowerShell](https://microsoft.com/PowerShell)

### Optional Dependencies
1. **nConvert**: Required for JPEG to WebP conversion
   - Download from [XnView.com](https://www.xnview.com/en/nconvert/)
   - Place `nconvert.exe` in your system PATH
   - Requires `libwebp.dll` in the "Plugins" subfolder

## Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/wesellis/CBR-to-CBZ-Converter.git
   cd CBR-to-CBZ-Converter
   ```

2. **Install dependencies** as listed in the Requirements section

3. **Verify setup** by running the following commands in PowerShell:
   ```powershell
   7z  # Should show 7-Zip help
   nconvert  # Should show nConvert help (if WebP conversion needed)
   ```

## Usage

### Basic Conversion
1. Navigate to the directory containing your CBR files
2. Copy `ConverterPS.ps1` to that directory
3. Run the script:
   ```powershell
   .\ConverterPS.ps1
   ```
4. Choose whether to convert JPEG images to WebP when prompted

### What the Script Does
1. **Analyzes** all CBR and CBZ files in the current directory
2. **Extracts** archives to a temporary directory (`C:\Temp\Convert-temp`)
3. **Converts** JPEG images to WebP format (if selected)
4. **Repackages** files into CBZ format
5. **Cleans up** temporary files
6. **Reports** conversion statistics and timing

### File Processing Order
1. Existing CBZ files (if WebP conversion is enabled)
2. All CBR files in the directory

## Configuration

The script includes several configurable parameters:

```powershell
# Number of parallel conversion tasks
$cores = 12

# Temporary directory for conversion
$temppath = "C:\Temp\Convert-temp"

# WebP quality setting (in nConvert command)
# -q 85 (85% quality - good balance of size/quality)
```

## Example Output

```
This script will convert all .cbr files in the current directory to .cbz
Converting jpg to webp (for both .cbr and .cbz) is included interactively as an option.

Press 'y' followed by ENTER to convert jpegs to webp: y

Processing CBZ files...
Processing CBR files...
Conversion completed.

Days              : 0
Hours             : 0
Minutes           : 2
Seconds           : 45
```

## Troubleshooting

### Common Issues

**7-Zip not found**
- Ensure 7-Zip is installed and `7z.exe` is in your PATH
- Test by running `7z` in PowerShell

**nConvert not found** (for WebP conversion)
- Install nConvert and add to PATH
- Ensure `libwebp.dll` is in the Plugins folder

**PowerShell version errors**
- Upgrade to PowerShell 7.1 or later
- The `-Parallel` parameter requires recent PowerShell versions

**Permission errors**
- Ensure write access to the temporary directory
- Run PowerShell as administrator if needed

### Performance Tips

- Adjust the `$cores` variable based on your system capabilities
- Use an SSD for the temporary directory for faster I/O
- Close unnecessary applications during large batch conversions

## File Formats

### Supported Input Formats
- **CBR** - Comic Book RAR (primary target)
- **CBZ** - Comic Book ZIP (for image optimization)

### Supported Image Formats
- **JPEG/JPG** - Input format for WebP conversion
- **WebP** - Output format for size optimization

### Output Format
- **CBZ** - Comic Book ZIP (standard ZIP archive)

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Wesley Ellis**  
Email: wes@wesellis.com  
GitHub: [wesellis](https://github.com/wesellis)

## Acknowledgments

- 7-Zip for archive handling
- nConvert/XnView for image conversion
- PowerShell team for parallel processing capabilities