# API Documentation

This document provides detailed information about the bot's commands, configuration options, and internal APIs.

## Commands Reference

### Basic Commands

#### `!gemini [question]`
**Aliases**: `!ai`, `!ask`, `!chat`  
**Cooldown**: 3 seconds  
**Description**: Generate text responses using Gemini AI  

**Usage**:
```
!gemini What is the capital of France?
!ai Explain quantum computing
!chat Tell me a joke
```

**Parameters**:
- `question` (required): The question or prompt for the AI

**Features**:
- Conversation memory (remembers previous messages)
- Automatic message splitting for long responses
- Input sanitization and validation

---

#### `!vision [description]`
**Aliases**: `!image`, `!analyze`, `!see`  
**Cooldown**: 5 seconds  
**Description**: Analyze images using Gemini Vision  

**Usage**:
```
!vision What's in this image?
!image Describe the colors and objects
!analyze (with image attachment)
```

**Parameters**:
- `description` (optional): Specific question about the image
- Image attachment (required): PNG, JPG, JPEG, GIF, or WEBP

**Limitations**:
- Maximum image size: 20MB
- Supported formats: PNG, JPG, JPEG, GIF, WEBP

---

#### `!reset`
**Aliases**: `!clear`, `!restart`  
**Cooldown**: 1 second  
**Description**: Reset your conversation history  

**Usage**:
```
!reset
!clear
```

---

#### `!cooldown_status`
**Aliases**: `!cd_status`  
**Cooldown**: None  
**Description**: Check your current cooldown status for all commands  

**Usage**:
```
!cooldown_status
```

### Advanced Commands

#### `!translate [language] [text]`
**Aliases**: `!trans`  
**Cooldown**: 2 seconds  
**Description**: Translate text to specified language  

**Usage**:
```
!translate Spanish Hello world
!trans French Good morning
!translate Japanese Thank you very much
```

**Parameters**:
- `language` (required): Target language name
- `text` (required): Text to translate

---

#### `!summarize [text]`
**Aliases**: `!summary`  
**Cooldown**: 4 seconds  
**Description**: Summarize long text content  

**Usage**:
```
!summarize [long text content here]
```

**Parameters**:
- `text` (required): Text to summarize (minimum 100 characters)

**Limitations**:
- Minimum text length: 100 characters
- Maximum text length: 4000 characters

---

#### `!code [language] [description]`
**Aliases**: `!generate`  
**Cooldown**: 3 seconds  
**Description**: Generate code in specified programming language  

**Usage**:
```
!code python function to calculate fibonacci
!generate javascript sort an array
!code java hello world program
```

**Parameters**:
- `language` (required): Programming language
- `description` (required): Description of what the code should do

---

#### `!imagine [description]`
**Aliases**: `!prompt`  
**Cooldown**: 3 seconds  
**Description**: Optimize prompts for image generation AI  

**Usage**:
```
!imagine a cat sitting on a rainbow
!prompt futuristic city at sunset
```

**Parameters**:
- `description` (required): Basic description for optimization

### Admin Commands

#### `!temperature [value]`
**Aliases**: `!temp`  
**Cooldown**: 1 second  
**Permission**: Admin only  
**Description**: Set Gemini API temperature value  

**Usage**:
```
!temperature 0.7
!temp 0.9
!temperature (shows current value)
```

**Parameters**:
- `value` (optional): Temperature value between 0.0 and 1.0

---

#### `!stats`
**Aliases**: `!statistics`  
**Permission**: Admin only  
**Description**: Show bot usage statistics  

**Usage**:
```
!stats
```

---

#### `!reset_all`
**Aliases**: `!clear_all`  
**Permission**: Admin only  
**Description**: Reset all user conversation histories  

**Usage**:
```
!reset_all
```

## Configuration Options

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Discord bot token |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `COMMAND_PREFIX` | No | Bot command prefix (default: !) |

### Config.py Settings

#### Cooldown Settings (seconds)
```python
COOLDOWN_GEMINI = 3
COOLDOWN_VISION = 5
COOLDOWN_TRANSLATE = 2
COOLDOWN_SUMMARIZE = 4
COOLDOWN_CODE = 3
COOLDOWN_IMAGINE = 3
COOLDOWN_RESET = 1
COOLDOWN_TEMPERATURE = 1
```

#### Permission Settings
```python
ADMIN_ROLE_NAMES = ["Admin", "Administrator", "Moderator", "Bot Admin"]
ADMIN_USER_IDS = []  # Add specific user IDs
```

#### Rate Limiting
```python
MAX_REQUESTS_PER_MINUTE = 20
MAX_MESSAGE_LENGTH = 4000
MAX_IMAGE_SIZE_MB = 20
```

#### AI Settings
```python
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40
MAX_OUTPUT_TOKENS = 2048
```

## Error Codes

| Error Type | Description | Solution |
|------------|-------------|----------|
| Cooldown | Command used too frequently | Wait for cooldown to expire |
| Permission | Insufficient permissions | Contact server admin |
| Rate Limit | Too many requests | Wait one minute |
| Invalid Input | Input validation failed | Check input format |
| API Error | Gemini API issue | Try again later |

## Rate Limits

- **Per User**: 20 requests per minute
- **Cooldowns**: Vary by command (1-5 seconds)
- **Admin Bypass**: Admins bypass cooldowns and rate limits
- **Image Size**: Maximum 20MB per image
