# 🤖 Gemini AI Discord Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini](https://img.shields.io/badge/Gemini-2.5-orange.svg)](https://ai.google.dev/)

A powerful Discord bot with advanced AI capabilities using Google's latest Gemini API. Bring cutting-edge AI features to your Discord server with easy setup and comprehensive functionality.

## ✨ Features

### 🧠 **Core AI Capabilities**
- **💬 Text Generation**: Chat with Gemini AI using natural language
- **👁️ Image Analysis**: Analyze and describe images with Gemini Vision
- **🧠 Conversation Memory**: Maintains context across conversations
- **🌐 Translation**: Translate text between multiple languages
- **📝 Text Summarization**: Summarize long content into key points
- **💻 Code Generation**: Generate code in various programming languages
- **🎨 Prompt Optimization**: Optimize prompts for image generation AI

### 🛡️ **Security & Performance**
- **⏰ Command Cooldowns**: Prevent spam with customizable cooldowns
- **🔐 Permission System**: Role-based access control
- **📊 Rate Limiting**: Intelligent request throttling
- **🛡️ Input Validation**: Comprehensive input sanitization
- **📝 Enhanced Logging**: Detailed logging for monitoring and debugging

### ⚙️ **Administration**
- **📊 Usage Statistics**: Monitor bot usage and performance
- **🔧 Dynamic Configuration**: Adjust settings without restart
- **👑 Admin Commands**: Powerful tools for server administrators
- **🔄 Conversation Management**: Reset individual or all conversations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord account with server admin permissions
- Google account for Gemini API access

### 1️⃣ Clone Repository
```bash
git clone https://github.com/MirLunaDEV/gemini-discord-bot.git
cd gemini-discord-bot
```

### 2️⃣ Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Configure Bot
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your tokens
# DISCORD_TOKEN=your_discord_bot_token
# GEMINI_API_KEY=your_gemini_api_key
```

### 4️⃣ Run Bot
```bash
# Method 1: Direct Python
python main.py

# Method 2: Windows Batch File
run.bat
```

> 📖 **Need detailed setup instructions?** Check out our [Installation Guide](docs/INSTALLATION.md)

## Getting API Keys

### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" to create a new application
3. Navigate to the "Bot" tab and click "Add Bot"
4. Click "Reset Token" to generate and copy the token
5. Enable "MESSAGE CONTENT INTENT"

### Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API key" to generate a new API key
4. Copy the generated API key

## Running the Bot

### Method 1: Direct Python execution
```bash
python main.py
```

### Method 2: Using Windows batch file
```bash
run.bat
```

## 📋 Commands

### 🎯 **Basic Commands**
| Command | Description | Cooldown | Example |
|---------|-------------|----------|---------|
| `!gemini [question]` | Chat with Gemini AI | 3s | `!gemini What is quantum computing?` |
| `!vision [description]` | Analyze images | 5s | `!vision What's in this image?` |
| `!reset` | Reset conversation history | 1s | `!reset` |
| `!help` | Show available commands | - | `!help` |
| `!cooldown_status` | Check command cooldowns | - | `!cooldown_status` |

### ⚡ **Advanced Commands**
| Command | Description | Cooldown | Example |
|---------|-------------|----------|---------|
| `!translate [lang] [text]` | Translate text | 2s | `!translate Spanish Hello world` |
| `!summarize [text]` | Summarize content | 4s | `!summarize [long text...]` |
| `!code [lang] [desc]` | Generate code | 3s | `!code python fibonacci function` |
| `!imagine [description]` | Optimize AI prompts | 3s | `!imagine a cat on a rainbow` |

### 👑 **Admin Commands**
| Command | Description | Permission | Example |
|---------|-------------|------------|---------|
| `!temperature [value]` | Set AI creativity | Admin | `!temperature 0.8` |
| `!stats` | Show bot statistics | Admin | `!stats` |
| `!reset_all` | Reset all conversations | Admin | `!reset_all` |

> 📖 **Want more details?** Check out our [API Documentation](docs/API.md) and [Usage Examples](examples/USAGE_EXAMPLES.md)

## ⚙️ Configuration

### Environment Variables
```env
DISCORD_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
COMMAND_PREFIX=!
```

### Customizable Settings (config.py)
```python
# Cooldown times (seconds)
COOLDOWN_GEMINI = 3
COOLDOWN_VISION = 5
COOLDOWN_TRANSLATE = 2

# Admin permissions
ADMIN_ROLE_NAMES = ["Admin", "Moderator"]
ADMIN_USER_IDS = []

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 20
MAX_MESSAGE_LENGTH = 4000
MAX_IMAGE_SIZE_MB = 20

# AI parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
MAX_OUTPUT_TOKENS = 2048
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](docs/INSTALLATION.md) | Detailed setup instructions |
| [API Documentation](docs/API.md) | Complete command reference |
| [Usage Examples](examples/USAGE_EXAMPLES.md) | Practical usage examples |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [Contributing](CONTRIBUTING.md) | How to contribute to the project |
| [Changelog](CHANGELOG.md) | Version history and changes |

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** - For providing the powerful AI capabilities
- **Discord.py** - For the excellent Discord API wrapper
- **Contributors** - Thank you to everyone who helps improve this project

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/MirLunaDEV/gemini-discord-bot/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/MirLunaDEV/gemini-discord-bot/discussions)
- 📖 **Documentation**: Check the [docs](docs/) folder
- ❓ **Questions**: Open a discussion or check existing issues

---

**⭐ If you find this project helpful, please consider giving it a star on GitHub!**

Made with ❤️ by the community
