import discord
import json
import os
import time
import asyncio
from typing import Dict, List, Optional, Set
import logging
import config

logger = logging.getLogger('gemini-discord-bot.utils')

class CooldownManager:
    """Manages command cooldowns for users"""

    def __init__(self):
        self.cooldowns: Dict[str, Dict[int, float]] = {}

    def is_on_cooldown(self, command: str, user_id: int, cooldown_time: float) -> bool:
        """Check if user is on cooldown for a command"""
        current_time = time.time()

        if command not in self.cooldowns:
            self.cooldowns[command] = {}

        if user_id not in self.cooldowns[command]:
            return False

        last_used = self.cooldowns[command][user_id]
        return (current_time - last_used) < cooldown_time

    def get_remaining_cooldown(self, command: str, user_id: int, cooldown_time: float) -> float:
        """Get remaining cooldown time in seconds"""
        if not self.is_on_cooldown(command, user_id, cooldown_time):
            return 0.0

        current_time = time.time()
        last_used = self.cooldowns[command][user_id]
        return cooldown_time - (current_time - last_used)

    def set_cooldown(self, command: str, user_id: int):
        """Set cooldown for user and command"""
        current_time = time.time()

        if command not in self.cooldowns:
            self.cooldowns[command] = {}

        self.cooldowns[command][user_id] = current_time

    def clear_cooldown(self, command: str, user_id: int):
        """Clear cooldown for user and command"""
        if command in self.cooldowns and user_id in self.cooldowns[command]:
            del self.cooldowns[command][user_id]

class PermissionManager:
    """Manages user permissions and roles"""

    @staticmethod
    def is_admin(member: discord.Member) -> bool:
        """Check if member has admin permissions"""
        if member.guild_permissions.administrator:
            return True

        if member.id in config.ADMIN_USER_IDS:
            return True

        for role in member.roles:
            if role.name in config.ADMIN_ROLE_NAMES:
                return True

        return False

    @staticmethod
    def can_use_command(member: discord.Member, command_name: str) -> bool:
        """Check if member can use a specific command"""
        # Admin commands
        admin_commands = ["temperature", "reset_all", "stats"]

        if command_name in admin_commands:
            return PermissionManager.is_admin(member)

        return True

class RateLimiter:
    """Rate limiting for API calls and commands"""

    def __init__(self):
        self.user_requests: Dict[int, List[float]] = {}

    def is_rate_limited(self, user_id: int) -> bool:
        """Check if user is rate limited"""
        current_time = time.time()

        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        # Remove old requests (older than 1 minute)
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id]
            if current_time - req_time < 60
        ]

        return len(self.user_requests[user_id]) >= config.MAX_REQUESTS_PER_MINUTE

    def add_request(self, user_id: int):
        """Add a request for user"""
        current_time = time.time()

        if user_id not in self.user_requests:
            self.user_requests[user_id] = []

        self.user_requests[user_id].append(current_time)

class InputValidator:
    """Validates user inputs"""

    @staticmethod
    def validate_text_length(text: str, max_length: int = None) -> bool:
        """Validate text length"""
        if max_length is None:
            max_length = config.MAX_MESSAGE_LENGTH

        return len(text) <= max_length

    @staticmethod
    def validate_temperature(value: float) -> bool:
        """Validate temperature value"""
        return 0.0 <= value <= 1.0

    @staticmethod
    def validate_image_size(file_size: int) -> bool:
        """Validate image file size"""
        max_size_bytes = config.MAX_IMAGE_SIZE_MB * 1024 * 1024
        return file_size <= max_size_bytes

    @staticmethod
    def sanitize_input(text: str) -> str:
        """Sanitize user input"""
        # Remove potential harmful characters
        dangerous_chars = ['`', '@everyone', '@here']

        for char in dangerous_chars:
            text = text.replace(char, '')

        return text.strip()

class ErrorHandler:
    """Enhanced error handling"""

    @staticmethod
    async def handle_api_error(ctx, error: Exception, api_name: str = "API"):
        """Handle API errors with user-friendly messages"""
        error_msg = str(error).lower()

        if "quota" in error_msg or "limit" in error_msg:
            await ctx.send(f"❌ {api_name} quota exceeded. Please try again later.")
        elif "invalid" in error_msg or "unauthorized" in error_msg:
            await ctx.send(f"❌ {api_name} authentication error. Please check configuration.")
        elif "timeout" in error_msg:
            await ctx.send(f"❌ {api_name} request timed out. Please try again.")
        elif "network" in error_msg or "connection" in error_msg:
            await ctx.send(f"❌ Network error. Please check your connection and try again.")
        else:
            await ctx.send(f"❌ An unexpected error occurred. Please try again later.")

        logger.error(f"{api_name} error for user {ctx.author.id}: {str(error)}")

    @staticmethod
    async def handle_cooldown_error(ctx, remaining_time: float):
        """Handle cooldown errors"""
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        if minutes > 0:
            time_str = f"{minutes}m {seconds}s"
        else:
            time_str = f"{seconds}s"

        await ctx.send(f"⏰ Command is on cooldown. Try again in {time_str}.")

    @staticmethod
    async def handle_permission_error(ctx, command_name: str):
        """Handle permission errors"""
        await ctx.send(f"❌ You don't have permission to use the `{command_name}` command.")

    @staticmethod
    async def handle_rate_limit_error(ctx):
        """Handle rate limit errors"""
        await ctx.send(f"❌ You're sending commands too quickly. Please slow down and try again in a minute.")

class ConversationManager:
    """Manages conversation history for each user"""

    def __init__(self, storage_path: str = "conversations", max_history: int = 10):
        self.storage_path = storage_path
        self.max_history = max_history
        self.conversations: Dict[int, List[Dict[str, str]]] = {}

        os.makedirs(self.storage_path, exist_ok=True)
        self._load_conversations()

    def _get_user_file_path(self, user_id: int) -> str:
        """Get file path for user ID"""
        return os.path.join(self.storage_path, f"{user_id}.json")

    def _load_conversations(self) -> None:
        """Load all saved conversations"""
        try:
            for filename in os.listdir(self.storage_path):
                if filename.endswith(".json"):
                    user_id = int(filename.split(".")[0])
                    file_path = os.path.join(self.storage_path, filename)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.conversations[user_id] = json.load(f)
                    except Exception as e:
                        logger.error(f"Error loading conversation for user {user_id}: {str(e)}")
        except Exception as e:
            logger.error(f"Error loading conversations: {str(e)}")

    def _save_conversation(self, user_id: int) -> None:
        """Save user conversation"""
        try:
            file_path = self._get_user_file_path(user_id)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversations[user_id], f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving conversation for user {user_id}: {str(e)}")

    def get_conversation(self, user_id: int) -> List[Dict[str, str]]:
        """Get user conversation history"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []

        return self.conversations[user_id]

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """Add message to conversation"""
        if user_id not in self.conversations:
            self.conversations[user_id] = []

        self.conversations[user_id].append({"role": role, "parts": [content]})

        if len(self.conversations[user_id]) > self.max_history * 2:
            self.conversations[user_id] = self.conversations[user_id][-self.max_history * 2:]

        self._save_conversation(user_id)

    def reset_conversation(self, user_id: int) -> None:
        """Reset user conversation history"""
        self.conversations[user_id] = []
        self._save_conversation(user_id)

class EmbedBuilder:
    """Helper class for creating Discord embeds"""

    @staticmethod
    def create_info_embed(title: str, description: str) -> discord.Embed:
        """Create info embed"""
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.blue()
        )

    @staticmethod
    def create_error_embed(title: str, description: str) -> discord.Embed:
        """Create error embed"""
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.red()
        )

    @staticmethod
    def create_success_embed(title: str, description: str) -> discord.Embed:
        """Create success embed"""
        return discord.Embed(
            title=title,
            description=description,
            color=discord.Color.green()
        )

    @staticmethod
    def create_gemini_response_embed(user: discord.User, prompt: str, response: str) -> discord.Embed:
        """Create Gemini response embed"""
        embed = discord.Embed(
            title="Gemini AI Response",
            color=discord.Color.purple()
        )

        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

        if len(prompt) > 1024:
            prompt = prompt[:1021] + "..."
        embed.add_field(name="Question", value=prompt, inline=False)

        if len(response) > 4096:
            response = response[:4093] + "..."
            embed.description = response
        else:
            embed.description = response

        embed.set_footer(text="Powered by Google Gemini AI")

        return embed

def split_long_message(message: str, max_length: int = 2000) -> List[str]:
    """Split long messages to fit Discord message length limit"""
    if len(message) <= max_length:
        return [message]

    chunks = []
    for i in range(0, len(message), max_length):
        chunks.append(message[i:i+max_length])

    return chunks
