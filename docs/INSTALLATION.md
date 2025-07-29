# Installation Guide

This guide will walk you through setting up the Gemini AI Discord Bot step by step.

## Prerequisites

- **Python 3.8 or higher**
- **Discord account** with server admin permissions
- **Google account** for Gemini API access
- **Git** (optional, for cloning)

## Step 1: Download the Bot

### Option A: Clone with Git
```bash
git clone https://github.com/yourusername/gemini-discord-bot.git
cd gemini-discord-bot
```

### Option B: Download ZIP
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Navigate to the extracted folder

## Step 2: Set Up Python Environment

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Get API Keys

### Discord Bot Token

1. **Go to Discord Developer Portal**
   - Visit: https://discord.com/developers/applications
   - Sign in with your Discord account

2. **Create New Application**
   - Click "New Application"
   - Enter a name for your bot
   - Click "Create"

3. **Create Bot**
   - Go to "Bot" tab in the left sidebar
   - Click "Add Bot"
   - Confirm by clicking "Yes, do it!"

4. **Get Token**
   - Under "Token" section, click "Reset Token"
   - Copy the token (keep it secret!)

5. **Set Permissions**
   - Scroll down to "Privileged Gateway Intents"
   - Enable "Message Content Intent"
   - Save changes

### Gemini API Key

1. **Go to Google AI Studio**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account

2. **Create API Key**
   - Click "Get API key"
   - Click "Create API key in new project" (or select existing project)
   - Copy the generated API key

## Step 4: Configure Environment

### Create .env File
```bash
cp .env.example .env
```

### Edit .env File
Open `.env` in a text editor and fill in your keys:
```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Bot Configuration
COMMAND_PREFIX=!
```

## Step 5: Invite Bot to Server

### Generate Invite Link

1. **Go to OAuth2 → URL Generator**
   - In Discord Developer Portal
   - Select your application

2. **Select Scopes**
   - Check "bot"
   - Check "applications.commands" (optional)

3. **Select Bot Permissions**
   - Send Messages
   - Read Message History
   - Use Slash Commands (optional)
   - Embed Links
   - Attach Files
   - Read Messages/View Channels

4. **Copy and Use URL**
   - Copy the generated URL
   - Open it in browser
   - Select your server
   - Authorize the bot

## Step 6: Run the Bot

### Method 1: Python Command
```bash
python main.py
```

### Method 2: Windows Batch File
```bash
run.bat
```

### Verify Bot is Running
- Check console for "Bot is ready!" message
- Bot should appear online in your Discord server
- Try `!help` command

## Step 7: Test the Bot

### Basic Test Commands
```
!help                    # Show help menu
!gemini Hello!          # Test AI chat
!cooldown_status        # Check cooldowns
```

### Test with Image (if you have one)
```
!vision                 # Upload an image with this command
```

## Troubleshooting

### Common Issues

#### Bot Not Responding
- **Check token**: Ensure Discord token is correct
- **Check permissions**: Bot needs "Send Messages" permission
- **Check prefix**: Default is `!`, make sure you're using correct prefix

#### "Invalid API Key" Error
- **Check Gemini key**: Ensure API key is correct and active
- **Check quotas**: Verify you haven't exceeded API limits

#### Import Errors
- **Check Python version**: Must be 3.8+
- **Reinstall dependencies**: `pip install -r requirements.txt`
- **Check virtual environment**: Make sure it's activated

#### Permission Errors
- **Bot role position**: Bot's role should be above roles it needs to manage
- **Channel permissions**: Check channel-specific permissions

### Getting Help

1. **Check logs**: Look at console output for error messages
2. **Check documentation**: Review [API.md](API.md) for command details
3. **GitHub Issues**: Report bugs or ask questions
4. **Discord permissions**: Verify bot has necessary permissions

## Advanced Configuration

### Custom Settings

Edit `config.py` to customize:
- Cooldown times
- Admin roles
- Rate limits
- AI parameters

### Admin Setup

Add admin roles or user IDs in `config.py`:
```python
ADMIN_ROLE_NAMES = ["Admin", "Moderator", "Bot Admin"]
ADMIN_USER_IDS = [123456789012345678]  # Your Discord user ID
```

### Logging

Logs are saved to `bot.log`. To change log level, edit `config.py`:
```python
LOG_LEVEL = "DEBUG"  # INFO, WARNING, ERROR
```

## Security Notes

- **Keep tokens secret**: Never share your Discord token or API keys
- **Use .env file**: Don't hardcode tokens in source code
- **Regular updates**: Keep dependencies updated
- **Monitor usage**: Check API usage to avoid unexpected charges

## Next Steps

- Read [API.md](API.md) for detailed command documentation
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) if you want to contribute
- Join our community for support and updates

Congratulations! Your Gemini AI Discord Bot is now ready to use! 🎉
