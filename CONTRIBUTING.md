# Contributing to CBR to CBZ Converter

Thank you for your interest in contributing to the CBR to CBZ Converter project! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and professional environment for all contributors.

## How to Contribute

### Reporting Issues

Before creating an issue, please:
1. Check if the issue has already been reported
2. Provide clear and detailed information about the problem
3. Include system information (OS, PowerShell version, 7-Zip version)
4. Provide steps to reproduce the issue

### Suggesting Enhancements

We welcome suggestions for improvements! Please:
1. Check if the enhancement has already been suggested
2. Provide a clear description of the proposed feature
3. Explain why this enhancement would be useful
4. Consider the impact on existing functionality

### Pull Requests

1. **Fork the repository** and create your feature branch from `main`
2. **Write clear, descriptive commit messages**
3. **Test your changes** thoroughly
4. **Update documentation** as needed
5. **Follow PowerShell best practices**
6. **Ensure your code is properly commented**

### Development Guidelines

#### PowerShell Standards
- Use approved PowerShell verbs
- Include comprehensive help documentation
- Implement proper error handling
- Use meaningful variable names
- Follow PowerShell formatting conventions

#### Code Style
- Use 4-space indentation
- Keep lines under 120 characters when possible
- Use consistent naming conventions
- Add comments for complex logic

#### Testing
- Test with different file sizes and types
- Verify functionality on different Windows versions
- Test both CBR to CBZ and JPEG to WebP conversions
- Ensure temporary file cleanup works correctly

## Development Setup

### Prerequisites
- PowerShell 7.1 or later
- 7-Zip installed with 7z.exe in PATH
- nConvert (for WebP conversion testing)
- Git for version control

### Local Development
1. Fork and clone the repository
2. Create a test directory with sample CBR files
3. Test your changes thoroughly
4. Ensure all temporary files are cleaned up

## Submission Guidelines

### Commit Messages
Use clear, descriptive commit messages:
```
Add support for CB7 format conversion

- Implement CB7 to CBZ conversion
- Update documentation with new format support
- Add error handling for unsupported archives
```

### Pull Request Process
1. Update the CHANGELOG.md with your changes
2. Update documentation if needed
3. Ensure your code follows the style guidelines
4. Test thoroughly before submitting
5. Provide a clear description of your changes

## Recognition

Contributors will be acknowledged in the project documentation and release notes.

## Questions?

If you have questions about contributing, please:
- Open an issue with the "question" label
- Contact Wesley Ellis at wes@wesellis.com

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to CBR to CBZ Converter!