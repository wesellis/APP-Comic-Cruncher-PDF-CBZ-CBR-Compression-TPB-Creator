# Changelog

All notable changes to Comic Cruncher will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-06-18

### Added
- **Comic Combiner Mode**: Complete new functionality for creating Trade Paperback collections
- **Dual-mode interface**: Toggle between Cruncher and Combiner modes
- **Series pattern detection**: Automatic identification of comic series and issue numbers
- **TPB auto-creation**: Groups 12 issues into volumes with proper naming
- **Smart batch processing**: Handles multiple files with parallel processing
- **Activity feed**: Real-time processing updates and batch summaries
- **File size reporting**: Shows compression ratios and space saved
- **Enhanced progress tracking**: Mode-specific progress indicators
- **Intelligent series naming**: Multiple regex patterns for issue detection
- **Auto-cleanup**: Removes original issues after successful combination

### Enhanced
- **UI redesign**: Modern dual-mode interface with toggle buttons
- **Drag-and-drop**: Now supports both files and directories
- **Progress visualization**: Dynamic labels based on current mode
- **Error handling**: Better feedback for processing issues
- **Memory optimization**: Improved handling of large batches

### Technical Improvements
- **Parallel image processing**: Full CPU utilization for batch operations
- **Thread management**: Separate threads for different processing modes
- **Pattern recognition**: Advanced regex for comic series identification
- **Volume management**: Intelligent grouping and naming of TPB collections
- **File safety**: Enhanced backup and cleanup procedures

## [1.0.0] - 2025-05-01

### Added
- **Core compression functionality**: PDF, CBZ, CBR to optimized CBZ
- **WebP conversion**: 85% quality with size optimization
- **Smart resizing**: Max 2500×2500 maintaining aspect ratio
- **Parallel processing**: Multi-core CPU utilization
- **Safe backup system**: Automatic .backup file creation
- **Modern PyQt6 interface**: Drag-and-drop with progress tracking
- **Cross-platform support**: Windows, Linux, macOS compatibility
- **Batch processing support**: Multiple file handling
- **Smart skip detection**: Avoids re-processing optimized files

### Installation Tools
- **install.bat**: Automated Windows installation
- **run.bat**: Windows launcher with error checking
- **fix_dependencies.bat**: Troubleshooting utility
- **requirements.txt**: Python dependency specification

### Initial Features
- **Universal format support**: Handles PDF, CBZ, and CBR inputs
- **Progress visualization**: Real-time processing feedback
- **Error handling**: Graceful failure with user notification
- **File validation**: Input format verification
- **Temporary file management**: Clean handling of processing files

## [Development History]

### Pre-1.0 Development
- Initial concept as CBR-to-CBZ converter
- Basic PyQt5 interface development
- Single-threaded processing implementation
- PDF support addition via pdf2image
- Parallel processing implementation
- UI/UX design and polish
- Windows installation automation
- Cross-platform compatibility testing

---

## Release Notes

### Version 2.0.0 - "Comic Combiner Edition"

This major release transforms Comic Cruncher from a single-purpose compression tool into a comprehensive comic processing suite. The addition of Comic Combiner mode provides a complete solution for both optimizing individual comics and creating organized TPB collections.

**Key Highlights:**
- **Dual functionality**: One application handles both compression and collection creation
- **Intelligent automation**: Auto-detects series patterns and creates properly named TPBs
- **Enhanced performance**: Improved batch processing with better resource management
- **Professional interface**: Modern toggle-based design with comprehensive progress tracking

**Breaking Changes:**
None - all existing functionality preserved and enhanced.

**Migration Notes:**
Existing users can continue using Cruncher mode exactly as before. Combiner mode is a new addition that doesn't affect existing workflows.

---

## Upcoming Features (Roadmap)

### Version 2.1.0 (Planned)
- **Custom TPB sizing**: User-configurable issues per volume
- **Series preferences**: Save and reuse series-specific settings
- **Enhanced pattern recognition**: Support for more naming conventions
- **Undo functionality**: Rollback recent operations

### Version 2.2.0 (Planned)
- **Configuration file**: Persistent user preferences
- **Quality profiles**: Predefined compression settings
- **Command-line interface**: Batch operations via CLI
- **Plugin system**: Extensible processing modules

### Version 3.0.0 (Future)
- **Comic reader integration**: Direct export to reading applications
- **Cloud storage support**: Direct processing from cloud services
- **Advanced metadata**: Comic information extraction and preservation
- **Internationalization**: Multi-language interface support
