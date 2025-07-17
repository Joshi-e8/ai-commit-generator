# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-01-17

### Fixed
- Fixed urllib3 compatibility issue by replacing deprecated `method_whitelist` with `allowed_methods` in Retry configuration
- Resolved "Retry.__init__() got an unexpected keyword argument 'method_whitelist'" error

## [1.0.1] - 2025-01-17

### Changed
- Updated package description to include GitHub repository URL
- Improved package metadata for better discoverability

### Fixed
- Updated CLI command references in documentation from `ai-commit-generator` to `smart-commits-ai`

## [1.0.0] - 2025-01-17

### Added
- Initial release of Smart Commits AI
- AI-powered commit message generation using Groq, OpenRouter, and Cohere APIs
- Support for conventional commit format
- Git hook integration for automatic commit message generation
- Rich CLI interface with comprehensive commands
- Configurable settings via YAML files and environment variables
- Multiple AI provider support with fallback mechanisms
- Comprehensive test suite
- Professional packaging and PyPI distribution

### Features
- **CLI Commands**:
  - `install` - Install Git hook in repository
  - `uninstall` - Remove Git hook
  - `status` - Show installation and configuration status
  - `generate` - Generate commit message for staged changes
  - `test` - Test with current staged changes
  - `config` - Manage configuration settings

- **AI Providers**:
  - Groq (recommended, free tier available)
  - OpenRouter (premium models)
  - Cohere (enterprise-focused)

- **Configuration**:
  - Customizable commit types and scopes
  - Adjustable message length limits
  - File exclusion patterns
  - Debug mode support
  - Environment variable support

- **Quality Assurance**:
  - Type hints throughout codebase
  - Comprehensive error handling
  - Retry mechanisms for API calls
  - Input validation and sanitization
  - Professional logging

### Technical Details
- Python 3.8+ support
- Modern packaging with pyproject.toml
- Rich CLI with colored output and progress indicators
- Robust Git integration
- Secure API key handling
- Cross-platform compatibility (Windows, macOS, Linux)

### Documentation
- Comprehensive README with examples
- API documentation with type hints
- Usage examples and configuration guides
- Professional PyPI package page

---

## Release Notes

### Version 1.0.1
This is a maintenance release that improves package metadata and documentation. The GitHub repository URL is now prominently displayed in the package description for better discoverability.

### Version 1.0.0
This is the initial stable release of Smart Commits AI. The package provides a complete solution for AI-powered Git commit message generation with support for multiple AI providers and comprehensive configuration options.

The tool is production-ready and has been thoroughly tested across different platforms and Git workflows. It follows Python packaging best practices and provides a professional CLI experience.

---

## Migration Guide

### From ai-commit-generator to smart-commits-ai
If you were using a previous version with the old package name:

1. Uninstall the old package: `pip uninstall ai-commit-generator`
2. Install the new package: `pip install smart-commits-ai`
3. Update CLI commands: `ai-commit-generator` → `smart-commits-ai`
4. Configuration files and settings remain the same

---

## Support

- **Issues**: [GitHub Issues](https://github.com/Joshi-e8/ai-commit-generator/issues)
- **Documentation**: [GitHub Repository](https://github.com/Joshi-e8/ai-commit-generator)
- **PyPI**: [Package Page](https://pypi.org/project/smart-commits-ai/)
