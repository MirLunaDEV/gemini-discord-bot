# Troubleshooting Guide

This guide helps you resolve common issues with the Gemini AI Discord Bot.

## Quick Diagnostics

### Check Bot Status
1. **Console Output**: Look for "Bot is ready!" message
2. **Discord Status**: Bot should show as online
3. **Response Test**: Try `!help` command

### Check Configuration
1. **Environment Variables**: Verify `.env` file exists and has correct values
2. **Permissions**: Ensure bot has necessary Discord permissions
3. **API Keys**: Verify both Discord and Gemini API keys are valid

## Common Issues

### 🤖 Bot Not Starting

#### Symptoms
- Console shows errors on startup
- Bot doesn't appear online in Discord
- Python script exits immediately

#### Solutions

**Check Python Version**
```bash
python --version  # Should be 3.8+
```

**Check Dependencies**
```bash
pip install -r requirements.txt
```

**Check Environment File**
- Ensure `.env` file exists
- Verify no extra spaces around `=`
- Check for special characters in tokens

**Check Discord Token**
- Token should be 59+ characters long
- No spaces or quotes around token
- Token should start with letters/numbers

---

### 🚫 Bot Not Responding to Commands

#### Symptoms
- Bot is online but doesn't respond
- No error messages in console
- Commands seem to be ignored

#### Solutions

**Check Command Prefix**
```bash
# Default is !
!help

# If you changed it in .env
?help  # or whatever prefix you set
```

**Check Bot Permissions**
Required permissions:
- Send Messages
- Read Message History
- Embed Links
- Attach Files
- Use External Emojis

**Check Channel Permissions**
- Bot can see the channel
- Bot can send messages in channel
- No channel-specific restrictions

**Check Role Hierarchy**
- Bot's role should be above roles it needs to interact with
- Move bot role higher in server settings

---

### 🔑 API Key Issues

#### Symptoms
- "Invalid API key" errors
- "Authentication failed" messages
- API quota exceeded warnings

#### Solutions

**Discord Token Issues**
```bash
# Check token format (example format only)
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE_59_CHARACTERS_LONG
```

**Gemini API Key Issues**
```bash
# Check key format (example format only)
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

**API Quota Problems**
- Check Google Cloud Console for quota limits
- Verify billing is enabled (if required)
- Monitor API usage

---

### ⏰ Cooldown and Rate Limit Issues

#### Symptoms
- "Command is on cooldown" messages
- "Too many requests" errors
- Commands not working for some users

#### Solutions

**Check Cooldown Status**
```bash
!cooldown_status
```

**Admin Bypass**
- Admins bypass cooldowns
- Check admin configuration in `config.py`

**Adjust Cooldown Times**
Edit `config.py`:
```python
COOLDOWN_GEMINI = 3  # Reduce if needed
```

---

### 🖼️ Image Analysis Issues

#### Symptoms
- "Could not download image" errors
- "Unsupported format" messages
- Vision commands not working

#### Solutions

**Check Image Format**
Supported formats:
- PNG
- JPG/JPEG
- GIF
- WEBP

**Check Image Size**
- Maximum: 20MB
- Reduce image size if too large

**Check Image URL**
- Image must be directly attached to Discord message
- External links may not work

---

### 💾 Memory and Performance Issues

#### Symptoms
- Bot becomes slow over time
- High memory usage
- Commands timing out

#### Solutions

**Restart Bot Regularly**
```bash
# Stop bot (Ctrl+C)
# Start again
python main.py
```

**Clear Conversation History**
```bash
!reset_all  # Admin only
```

**Check System Resources**
- Available RAM
- CPU usage
- Disk space

---

### 🔧 Configuration Issues

#### Symptoms
- Features not working as expected
- Permission errors for normal users
- Admin commands not accessible

#### Solutions

**Check Admin Configuration**
```python
# In config.py
ADMIN_ROLE_NAMES = ["Admin", "Moderator"]
ADMIN_USER_IDS = [123456789012345678]
```

**Check Feature Flags**
```python
# In config.py
ENABLE_IMAGE_ANALYSIS = True
ENABLE_CONVERSATION_MEMORY = True
```

**Reset Configuration**
- Copy from `config.py.example` if available
- Check for typos in variable names

## Error Messages

### Common Error Codes

| Error | Meaning | Solution |
|-------|---------|----------|
| `403 Forbidden` | Missing permissions | Check bot permissions |
| `401 Unauthorized` | Invalid token | Verify API keys |
| `429 Too Many Requests` | Rate limited | Wait and try again |
| `400 Bad Request` | Invalid input | Check command format |
| `500 Internal Server Error` | API issue | Try again later |

### Discord.py Errors

**`discord.errors.LoginFailure`**
- Invalid Discord token
- Check token in `.env` file

**`discord.errors.Forbidden`**
- Missing permissions
- Check bot role and permissions

**`aiohttp.ClientError`**
- Network connectivity issues
- Check internet connection

### Gemini API Errors

**`google.api_core.exceptions.Unauthenticated`**
- Invalid Gemini API key
- Check key in `.env` file

**`google.api_core.exceptions.ResourceExhausted`**
- API quota exceeded
- Check Google Cloud Console

## Debugging Tips

### Enable Debug Logging

Edit `config.py`:
```python
LOG_LEVEL = "DEBUG"
```

### Check Log Files

```bash
# View recent logs
tail -f bot.log

# Search for errors
grep ERROR bot.log
```

### Test Individual Components

**Test Discord Connection**
```python
# Minimal test script
import discord
client = discord.Client()
client.run('your_token')
```

**Test Gemini API**
```python
# Test API key
import google.generativeai as genai
genai.configure(api_key='your_key')
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello')
print(response.text)
```

## Getting Help

### Before Asking for Help

1. **Check this guide** for your specific issue
2. **Search existing issues** on GitHub
3. **Collect information**:
   - Error messages
   - Bot version
   - Python version
   - Operating system
   - Steps to reproduce

### Where to Get Help

1. **GitHub Issues**: For bugs and feature requests
2. **GitHub Discussions**: For questions and community support
3. **Documentation**: Check all docs in `/docs` folder

### Reporting Bugs

Include this information:
- **Description**: What happened vs what you expected
- **Steps**: How to reproduce the issue
- **Environment**: OS, Python version, bot version
- **Logs**: Relevant error messages
- **Configuration**: Relevant config settings (remove sensitive data)

## Prevention Tips

### Regular Maintenance

- **Update dependencies** regularly
- **Monitor API usage** to avoid quota issues
- **Backup configuration** before making changes
- **Test changes** in development environment first

### Best Practices

- **Use version control** for configuration changes
- **Monitor logs** for early warning signs
- **Set up alerts** for critical errors
- **Document custom changes** for future reference

---

Still having issues? Don't hesitate to ask for help in our GitHub repository! 🤝
