# Project Structure

This document explains the organization and structure of the Gemini AI Discord Bot project.

## 📁 Directory Structure

```
gemini-discord-bot/
├── 📁 .github/                    # GitHub templates and workflows
│   ├── 📁 ISSUE_TEMPLATE/
│   │   ├── bug_report.md          # Bug report template
│   │   └── feature_request.md     # Feature request template
│   └── pull_request_template.md   # Pull request template
├── 📁 cogs/                       # Discord.py cogs (command modules)
│   ├── __init__.py               # Package initialization
│   └── advanced_commands.py      # Advanced AI commands
├── 📁 docs/                       # Documentation
│   ├── API.md                    # API and commands reference
│   ├── INSTALLATION.md           # Detailed installation guide
│   ├── PROJECT_STRUCTURE.md      # This file
│   └── TROUBLESHOOTING.md        # Common issues and solutions
├── 📁 examples/                   # Usage examples and demos
│   └── USAGE_EXAMPLES.md         # Practical usage examples
├── 📁 venv/                       # Python virtual environment
├── 📄 .env                       # Environment variables (not in git)
├── 📄 .env.example               # Environment variables template
├── 📄 .gitignore                 # Git ignore rules
├── 📄 bot.py                     # Main bot implementation
├── 📄 CHANGELOG.md               # Version history and changes
├── 📄 config.py                  # Configuration settings
├── 📄 CONTRIBUTING.md            # Contribution guidelines
├── 📄 LICENSE                    # MIT license
├── 📄 main.py                    # Bot entry point
├── 📄 README.md                  # Project overview and setup
├── 📄 requirements.txt           # Python dependencies
├── 📄 run.bat                    # Windows batch runner
└── 📄 utils.py                   # Utility classes and functions
```

## 📋 File Descriptions

### Core Files

#### `main.py`
- **Purpose**: Entry point for the bot application
- **Contents**: Basic setup, error handling, and bot initialization
- **Usage**: `python main.py` to start the bot

#### `bot.py`
- **Purpose**: Main bot implementation with core commands
- **Contents**: 
  - Basic commands (gemini, vision, reset, help)
  - Event handlers (on_ready)
  - Cooldown and permission management
  - Error handling integration

#### `config.py`
- **Purpose**: Centralized configuration management
- **Contents**:
  - Environment variable loading
  - Default settings and constants
  - Feature flags and limits
  - Admin permissions configuration

#### `utils.py`
- **Purpose**: Utility classes and helper functions
- **Contents**:
  - `CooldownManager`: Command cooldown handling
  - `PermissionManager`: User permission checking
  - `RateLimiter`: Request rate limiting
  - `InputValidator`: Input validation and sanitization
  - `ErrorHandler`: Centralized error handling
  - `ConversationManager`: Conversation history management
  - `EmbedBuilder`: Discord embed creation helpers

### Command Modules

#### `cogs/advanced_commands.py`
- **Purpose**: Advanced AI functionality commands
- **Contents**:
  - Translation commands
  - Text summarization
  - Code generation
  - Image prompt optimization
- **Architecture**: Discord.py Cog for modular command organization

### Configuration Files

#### `.env` / `.env.example`
- **Purpose**: Environment variables for sensitive data
- **Contents**:
  - Discord bot token
  - Gemini API key
  - Bot configuration options
- **Security**: `.env` is gitignored, `.env.example` is the template

#### `requirements.txt`
- **Purpose**: Python package dependencies
- **Contents**: All required packages with version constraints
- **Usage**: `pip install -r requirements.txt`

### Documentation

#### `README.md`
- **Purpose**: Project overview and quick start guide
- **Contents**:
  - Feature overview with badges
  - Quick installation steps
  - Command reference table
  - Configuration examples

#### `docs/API.md`
- **Purpose**: Comprehensive API and command documentation
- **Contents**:
  - Detailed command descriptions
  - Parameter specifications
  - Configuration options
  - Error codes and troubleshooting

#### `docs/INSTALLATION.md`
- **Purpose**: Step-by-step installation guide
- **Contents**:
  - Prerequisites and requirements
  - Detailed setup instructions
  - API key acquisition guides
  - Troubleshooting common setup issues

#### `docs/TROUBLESHOOTING.md`
- **Purpose**: Common issues and their solutions
- **Contents**:
  - Diagnostic procedures
  - Error message explanations
  - Configuration problems
  - Performance optimization tips

#### `CONTRIBUTING.md`
- **Purpose**: Guidelines for project contributors
- **Contents**:
  - Development setup instructions
  - Code style guidelines
  - Pull request process
  - Issue reporting guidelines

#### `CHANGELOG.md`
- **Purpose**: Version history and release notes
- **Contents**:
  - Feature additions and changes
  - Bug fixes and improvements
  - Breaking changes
  - Migration guides

### Examples and Templates

#### `examples/USAGE_EXAMPLES.md`
- **Purpose**: Practical usage examples and best practices
- **Contents**:
  - Command usage examples
  - Common use cases
  - Tips and tricks
  - Error handling examples

#### `.github/ISSUE_TEMPLATE/`
- **Purpose**: Standardized issue reporting templates
- **Contents**:
  - Bug report template
  - Feature request template
  - Structured information collection

#### `.github/pull_request_template.md`
- **Purpose**: Pull request template for consistent contributions
- **Contents**:
  - Change description format
  - Testing checklist
  - Review guidelines

## 🏗️ Architecture Overview

### Modular Design
- **Core Bot**: Essential functionality in `bot.py`
- **Extensions**: Advanced features in `cogs/`
- **Utilities**: Shared functionality in `utils.py`
- **Configuration**: Centralized settings in `config.py`

### Key Design Patterns

#### Command Pattern
- Commands organized as Discord.py commands and cogs
- Consistent parameter validation and error handling
- Modular and extensible architecture

#### Manager Pattern
- Separate managers for different concerns:
  - `CooldownManager`: Command timing
  - `PermissionManager`: Access control
  - `ConversationManager`: Chat history
  - `RateLimiter`: Request throttling

#### Decorator Pattern
- Permission and cooldown checking decorators
- Consistent behavior across commands
- Easy to apply to new commands

### Data Flow
1. **User Input** → Discord message
2. **Command Parsing** → Discord.py framework
3. **Validation** → Input validators and permission checks
4. **Processing** → Gemini API calls
5. **Response** → Formatted Discord messages

## 🔧 Development Guidelines

### Adding New Commands
1. Create command function in appropriate file
2. Add permission and cooldown decorators
3. Implement input validation
4. Add error handling
5. Update documentation

### Adding New Features
1. Design feature architecture
2. Update configuration if needed
3. Implement core functionality
4. Add tests and examples
5. Update documentation

### Code Organization
- Keep related functionality together
- Use descriptive names for functions and variables
- Add docstrings for all public functions
- Follow existing patterns and conventions

This structure ensures maintainability, extensibility, and ease of use for both developers and end users.
