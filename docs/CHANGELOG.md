# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/lang/zh-CN/) specification.

## [1.0.0] - 2024-01-01

### Added
- 🎉 Initial release
- ✨ Support for mainstream platforms: Douyin, Tencent Video, Bilibili, Xiaohongshu, TikTok, Kuaishou, etc.
- 🔧 Unified configuration management system (YAML + environment variables)
- 📝 Comprehensive documentation and usage guides
- 🛠️ CLI command line tool
- 📊 Log management system
- 🔐 Cookie management and validation
- ⏰ Scheduled publishing functionality
- 🎬 Video file processing

### Features
- **Multi-platform support**: One-click upload to multiple social media platforms
- **Flexible configuration**: Support for YAML configuration files and environment variable overrides
- **Cookie management**: Automatic cookie acquisition and validation for each platform
- **Scheduled publishing**: Support for timed publishing with customizable schedules
- **Video processing**: Automatic video format conversion and optimization
- **Logging system**: Comprehensive logging with file rotation and structured output
- **CLI interface**: Easy-to-use command line interface for non-developers
- **Error handling**: Robust error handling and retry mechanisms
- **Cross-platform**: Support for Windows, macOS, and Linux

### Technical Details
- Built with Python 3.8+
- Uses Playwright for browser automation
- Implements unified configuration management
- Supports multiple video formats
- Includes comprehensive error handling
- Provides detailed logging and monitoring

### Platform Support
- **Douyin**: Full automation with cookie management
- **Tencent Video**: Browser automation with local Chrome support
- **Bilibili**: Integration with biliup-rs for reliable uploads
- **Xiaohongshu**: Support for both local and server-side signatures
- **TikTok**: International platform support with custom thumbnails
- **Kuaishou**: Complete automation with scan code login

### Configuration
- YAML-based configuration system
- Environment variable support for sensitive data
- Platform-specific settings
- Browser path configuration
- Proxy support for international platforms
- Notification system integration

### Documentation
- Comprehensive README with platform-specific guides
- Configuration examples and templates
- Troubleshooting guides
- Development documentation
- API reference for developers

### License
- 📄 MIT License 