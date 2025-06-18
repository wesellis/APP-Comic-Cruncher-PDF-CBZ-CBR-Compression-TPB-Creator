# Contributing to Comic Cruncher

Thank you for your interest in contributing to Comic Cruncher! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create** a new branch for your feature/fix
4. **Make** your changes
5. **Test** thoroughly
6. **Submit** a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/CBR-to-CBZ-Converter.git
cd CBR-to-CBZ-Converter

# Install dependencies
pip install -r requirements.txt

# Run the application
python comic_cruncher.py
```

## Code Style

- Follow **PEP 8** Python style guidelines
- Use **meaningful variable names**
- Add **docstrings** for functions and classes
- Keep **functions focused** and reasonably sized
- Comment **complex logic**

## Areas for Contribution

### High Priority
- **Cross-platform compatibility** improvements
- **Performance optimizations** for large batches
- **Additional comic formats** (e.g., CBT, CBA)
- **Enhanced pattern recognition** for series detection
- **Memory usage optimization**

### Medium Priority
- **UI/UX improvements**
- **Better error handling and user feedback**
- **Configuration file support**
- **Undo/rollback functionality**
- **Advanced compression options**

### Low Priority
- **Plugin system** for custom processors
- **Command-line interface**
- **Internationalization**
- **Dark/light theme toggle**
- **Integration with comic readers**

## Testing

Before submitting a pull request:

1. **Test** with various comic formats (PDF, CBZ, CBR)
2. **Test** both Cruncher and Combiner modes
3. **Test** single file and batch processing
4. **Test** edge cases** (corrupted files, unusual naming)
5. **Test** on your target platform

### Test Files

Create a test suite with:
- Small PDF files
- CBZ files with different image formats
- CBR files with various compression
- Files with unusual naming patterns
- Corrupted/malformed files

## Submitting Changes

### Pull Request Process

1. **Create descriptive title** (e.g., "Add support for CBT format")
2. **Provide detailed description** of changes
3. **Reference any issues** being addressed
4. **Include test results** or screenshots if applicable
5. **Ensure all tests pass**

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for CBT comic format
fix: Resolve memory leak in batch processing
docs: Update installation instructions
refactor: Improve image processing pipeline
```

## Bug Reports

When reporting bugs, please include:

- **Operating system** and version
- **Python version**
- **Exact steps** to reproduce
- **Expected behavior**
- **Actual behavior**
- **Error messages** (full traceback)
- **Sample files** (if possible)

## Feature Requests

For feature requests, please describe:

- **Use case** and motivation
- **Proposed solution**
- **Alternative approaches** considered
- **Implementation complexity** estimate

## Code Review Guidelines

When reviewing code:

- **Be constructive** and helpful
- **Focus on the code**, not the person
- **Suggest improvements** when possible
- **Ask questions** for clarification
- **Appreciate good work**

## Architecture Overview

### Key Components

- **ComicProcessor**: Single file processing thread
- **BatchProcessor**: Multiple file processing thread
- **ComicCombiner**: TPB creation functionality
- **ImageProcessor**: Core image manipulation
- **DragDropFrame**: File input handling
- **ComicCruncher**: Main UI controller

### Threading Model

- **Main thread**: UI updates and user interaction
- **Worker threads**: File processing (CPU-intensive)
- **QThread signals**: Communication between threads

### File Processing Pipeline

1. **Input validation** and format detection
2. **Backup creation** for safety
3. **Image extraction** from source format
4. **Parallel processing** of images
5. **Archive creation** (CBZ output)
6. **Cleanup** and verification

## Release Process

1. **Update version** in relevant files
2. **Update README** with new features
3. **Test thoroughly** on all platforms
4. **Create release notes**
5. **Tag release** in Git
6. **Upload to GitHub** releases

## Questions?

If you have questions about contributing:

1. **Check existing issues** for similar questions
2. **Open a new issue** with the "question" label
3. **Be specific** about what you need help with

Thank you for contributing to Comic Cruncher!
