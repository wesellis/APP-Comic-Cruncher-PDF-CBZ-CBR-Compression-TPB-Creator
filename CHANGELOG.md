# Changelog

All notable changes to the CBR to CBZ Converter project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation and repository structure
- Professional .gitignore file
- CONTRIBUTING.md guidelines
- LICENSE file (MIT)
- Web-based documentation (index.html)

### Changed
- Updated README.md with better formatting and structure
- Improved code documentation and comments

## [1.1.0] - 2025-05-23

### Added
- Repository standardization and professional structure
- Comprehensive .gitignore for comic book conversion projects
- Detailed installation and usage documentation
- Web interface for documentation

### Changed
- Improved README formatting and clarity
- Enhanced script documentation

### Fixed
- Documentation formatting and structure

## [1.0.0] - 2024-12-01

### Added
- Initial release of CBR to CBZ converter
- PowerShell script for batch conversion
- Support for JPEG to WebP conversion
- Parallel processing for faster conversions
- Integration with 7-Zip for archive handling
- Integration with nConvert for image format conversion

### Features
- Converts CBR (Comic Book RAR) files to CBZ (Comic Book ZIP) format
- Optional JPEG to WebP compression for smaller file sizes
- Batch processing of multiple files
- Temporary file management
- Progress tracking and timing
- Automatic cleanup of temporary files

### Requirements
- PowerShell 7.1 or later
- 7-Zip with 7z.exe in PATH
- nConvert (optional, for WebP conversion)
- libwebp.dll plugin for nConvert