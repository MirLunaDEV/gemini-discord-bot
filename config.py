import os
from dotenv import load_dotenv

load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '!')

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Gemini Model Configuration
GEMINI_TEXT_MODEL = "gemini-2.5-flash"
GEMINI_PRO_MODEL = "gemini-2.5-pro"

# Bot Configuration
MAX_RESPONSE_LENGTH = 2000
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95
DEFAULT_TOP_K = 40
MAX_OUTPUT_TOKENS = 2048

# Feature Configuration
ENABLE_IMAGE_ANALYSIS = True
ENABLE_CONVERSATION_MEMORY = True
CONVERSATION_MEMORY_LIMIT = 10

# Cooldown Configuration (in seconds)
COOLDOWN_GEMINI = 3
COOLDOWN_VISION = 5
COOLDOWN_TRANSLATE = 2
COOLDOWN_SUMMARIZE = 4
COOLDOWN_CODE = 3
COOLDOWN_IMAGINE = 3
COOLDOWN_RESET = 1
COOLDOWN_TEMPERATURE = 1

# Permission Configuration
ADMIN_ROLE_NAMES = ["Admin", "Administrator", "Moderator", "Bot Admin"]
ADMIN_USER_IDS = []  # Add specific user IDs here

# Rate Limiting
MAX_REQUESTS_PER_MINUTE = 20
MAX_MESSAGE_LENGTH = 4000
MAX_IMAGE_SIZE_MB = 20

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = "bot.log"
LOG_MAX_SIZE_MB = 10
LOG_BACKUP_COUNT = 5
