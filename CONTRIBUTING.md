# Contributing to Gemini AI Discord Bot

Thank you for your interest in contributing to the Gemini AI Discord Bot! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Use the bug report template** when creating new issues
3. **Provide detailed information** including:
   - Bot version
   - Discord.py version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. **Check existing feature requests** to avoid duplicates
2. **Use the feature request template**
3. **Explain the use case** and why it would be beneficial
4. **Consider implementation complexity**

### Code Contributions

#### Prerequisites

- Python 3.8 or higher
- Basic knowledge of Discord.py
- Understanding of async/await patterns
- Familiarity with Google Gemini API

#### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/gemini-discord-bot.git
   cd gemini-discord-bot
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your tokens
   ```

#### Code Style

- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

#### Testing

- Test your changes thoroughly
- Ensure existing functionality still works
- Add tests for new features when possible
- Test with different Discord server configurations

#### Pull Request Process

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines

3. **Commit your changes**:
   ```bash
   git commit -m "Add: brief description of changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable

## 📋 Code Guidelines

### Command Development

- Use the cooldown and permission decorators
- Implement proper error handling
- Validate user inputs
- Provide helpful error messages
- Follow the existing command structure

### Error Handling

- Use the `ErrorHandler` class for consistent error messages
- Log errors appropriately
- Provide user-friendly feedback
- Handle API rate limits gracefully

### Configuration

- Add new settings to `config.py`
- Use environment variables for sensitive data
- Provide sensible defaults
- Document configuration options

## 🏷️ Commit Message Format

Use conventional commit format:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Example: `feat: add translation command with cooldown support`

## 📝 Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update configuration documentation
- Include usage examples

## ❓ Questions?

- Open a discussion on GitHub
- Check existing documentation
- Review similar implementations

Thank you for contributing! 🎉
