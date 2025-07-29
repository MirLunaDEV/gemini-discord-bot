import os
import discord
from discord.ext import commands
import google.generativeai as genai
import io
import aiohttp
from PIL import Image
import config
import logging
import asyncio
from typing import Dict, List, Optional, Union
from utils import (
    CooldownManager, PermissionManager, RateLimiter,
    InputValidator, ErrorHandler, split_long_message
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('gemini-discord-bot')

genai.configure(api_key=config.GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=config.COMMAND_PREFIX, intents=intents)

conversation_history: Dict[int, List[Dict[str, str]]] = {}

text_model = genai.GenerativeModel(config.GEMINI_TEXT_MODEL)
pro_model = genai.GenerativeModel(config.GEMINI_PRO_MODEL)

# Initialize managers
cooldown_manager = CooldownManager()
rate_limiter = RateLimiter()

def check_permissions_and_cooldown(cooldown_time: float):
    """Decorator to check permissions, cooldowns, and rate limits"""
    def decorator(func):
        async def wrapper(ctx, *args, **kwargs):
            # Check if user is rate limited
            if rate_limiter.is_rate_limited(ctx.author.id):
                await ErrorHandler.handle_rate_limit_error(ctx)
                return

            # Check permissions
            if not PermissionManager.can_use_command(ctx.author, func.__name__):
                await ErrorHandler.handle_permission_error(ctx, func.__name__)
                return

            # Check cooldown (skip for admins)
            if not PermissionManager.is_admin(ctx.author):
                if cooldown_manager.is_on_cooldown(func.__name__, ctx.author.id, cooldown_time):
                    remaining = cooldown_manager.get_remaining_cooldown(func.__name__, ctx.author.id, cooldown_time)
                    await ErrorHandler.handle_cooldown_error(ctx, remaining)
                    return

            # Set cooldown and add request
            cooldown_manager.set_cooldown(func.__name__, ctx.author.id)
            rate_limiter.add_request(ctx.author.id)

            # Execute command
            try:
                await func(ctx, *args, **kwargs)
            except Exception as e:
                await ErrorHandler.handle_api_error(ctx, e, "Gemini")

        return wrapper
    return decorator

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user.name} is ready!')

    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=f"{config.COMMAND_PREFIX}help"
    ))

    try:
        await load_cogs()
        logger.info("All cogs loaded successfully.")
    except Exception as e:
        logger.error(f"Error loading cogs: {str(e)}")

async def load_cogs():
    """Load all cogs from the cogs directory"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded cog: {filename}")
            except Exception as e:
                logger.error(f"Failed to load cog {filename}: {str(e)}")

@bot.command(name="gemini", aliases=["ai", "ask", "chat"])
@check_permissions_and_cooldown(config.COOLDOWN_GEMINI)
async def gemini_command(ctx, *, prompt: str = None):
    """Generate text responses using Gemini AI.

    Usage: !gemini [question or prompt]
    """
    if not prompt:
        await ctx.send(f"Usage: {config.COMMAND_PREFIX}gemini [question or prompt]")
        return

    # Validate input
    if not InputValidator.validate_text_length(prompt):
        await ctx.send(f"❌ Prompt is too long. Maximum length: {config.MAX_MESSAGE_LENGTH} characters.")
        return

    # Sanitize input
    prompt = InputValidator.sanitize_input(prompt)
    
    async with ctx.typing():
        user_id = ctx.author.id

        if config.ENABLE_CONVERSATION_MEMORY:
            if user_id not in conversation_history:
                conversation_history[user_id] = []

            conversation_history[user_id].append({"role": "user", "parts": [prompt]})

            if len(conversation_history[user_id]) > config.CONVERSATION_MEMORY_LIMIT * 2:
                conversation_history[user_id] = conversation_history[user_id][-config.CONVERSATION_MEMORY_LIMIT * 2:]

            chat = text_model.start_chat(history=conversation_history[user_id])
            response = chat.send_message(
                prompt,
                generation_config={
                    "temperature": config.DEFAULT_TEMPERATURE,
                    "top_p": config.DEFAULT_TOP_P,
                    "top_k": config.DEFAULT_TOP_K,
                    "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                }
            )

            conversation_history[user_id].append({"role": "model", "parts": [response.text]})
        else:
            response = text_model.generate_content(
                prompt,
                generation_config={
                    "temperature": config.DEFAULT_TEMPERATURE,
                    "top_p": config.DEFAULT_TOP_P,
                    "top_k": config.DEFAULT_TOP_K,
                    "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                }
            )

        response_text = response.text

        if len(response_text) > config.MAX_RESPONSE_LENGTH:
            chunks = split_long_message(response_text, config.MAX_RESPONSE_LENGTH)
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response_text)

@bot.command(name="vision", aliases=["image", "analyze", "see"])
@check_permissions_and_cooldown(config.COOLDOWN_VISION)
async def vision_command(ctx, *, prompt: Optional[str] = None):
    """Analyze images using Gemini Vision.

    Usage:
    - With image: !vision [description or question]
    - Image only: !vision
    """
    if not config.ENABLE_IMAGE_ANALYSIS:
        await ctx.send("❌ Image analysis feature is disabled.")
        return

    if not ctx.message.attachments:
        await ctx.send(f"❌ Please attach an image. Usage: {config.COMMAND_PREFIX}vision [description or question]")
        return

    attachment = ctx.message.attachments[0]

    # Validate file type
    if not any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']):
        await ctx.send("❌ Supported image formats: PNG, JPG, JPEG, GIF, WEBP")
        return

    # Validate file size
    if not InputValidator.validate_image_size(attachment.size):
        await ctx.send(f"❌ Image too large. Maximum size: {config.MAX_IMAGE_SIZE_MB}MB")
        return

    # Validate prompt if provided
    if prompt and not InputValidator.validate_text_length(prompt):
        await ctx.send(f"❌ Prompt is too long. Maximum length: {config.MAX_MESSAGE_LENGTH} characters.")
        return

    if prompt:
        prompt = InputValidator.sanitize_input(prompt)
    
    async with ctx.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ Could not download the image.")
                    return

                image_data = await resp.read()
                image = Image.open(io.BytesIO(image_data))

        if not prompt:
            prompt = "Please describe this image in detail."

        response = text_model.generate_content(
            [prompt, image],
            generation_config={
                "temperature": config.DEFAULT_TEMPERATURE,
                "top_p": config.DEFAULT_TOP_P,
                "top_k": config.DEFAULT_TOP_K,
                "max_output_tokens": config.MAX_OUTPUT_TOKENS,
            }
        )

        response_text = response.text

        if len(response_text) > config.MAX_RESPONSE_LENGTH:
            chunks = split_long_message(response_text, config.MAX_RESPONSE_LENGTH)
            for chunk in chunks:
                await ctx.send(chunk)
        else:
            await ctx.send(response_text)

@bot.command(name="reset", aliases=["clear", "restart"])
@check_permissions_and_cooldown(config.COOLDOWN_RESET)
async def reset_command(ctx):
    """Reset user's conversation history."""
    user_id = ctx.author.id

    if user_id in conversation_history:
        conversation_history[user_id] = []
        await ctx.send("✅ Conversation history has been reset.")
    else:
        await ctx.send("ℹ️ No conversation history to reset.")

@bot.command(name="temperature", aliases=["temp"])
@check_permissions_and_cooldown(config.COOLDOWN_TEMPERATURE)
async def temperature_command(ctx, value: float = None):
    """Set Gemini API temperature value (0.0 ~ 1.0).

    Usage: !temperature [value]
    """
    if value is None:
        await ctx.send(f"ℹ️ Current temperature value: {config.DEFAULT_TEMPERATURE}")
        return

    if not InputValidator.validate_temperature(value):
        await ctx.send("❌ Temperature value must be between 0.0 and 1.0.")
        return

    config.DEFAULT_TEMPERATURE = value
    await ctx.send(f"✅ Temperature value set to {value}.")

@bot.command(name="stats", aliases=["statistics"])
async def stats_command(ctx):
    """Show bot statistics (Admin only)."""
    if not PermissionManager.is_admin(ctx.author):
        await ErrorHandler.handle_permission_error(ctx, "stats")
        return

    total_users = len(conversation_history)
    total_conversations = sum(len(history) for history in conversation_history.values())

    embed = discord.Embed(
        title="📊 Bot Statistics",
        color=discord.Color.blue()
    )

    embed.add_field(name="Users with conversation history", value=total_users, inline=True)
    embed.add_field(name="Total conversation messages", value=total_conversations, inline=True)
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)

    await ctx.send(embed=embed)

@bot.command(name="reset_all", aliases=["clear_all"])
async def reset_all_command(ctx):
    """Reset all conversation histories (Admin only)."""
    if not PermissionManager.is_admin(ctx.author):
        await ErrorHandler.handle_permission_error(ctx, "reset_all")
        return

    conversation_history.clear()
    await ctx.send("✅ All conversation histories have been reset.")

@bot.command(name="cooldown_status", aliases=["cd_status"])
async def cooldown_status_command(ctx):
    """Check your current cooldown status."""
    user_id = ctx.author.id

    embed = discord.Embed(
        title="⏰ Your Cooldown Status",
        color=discord.Color.blue()
    )

    commands_cooldowns = {
        "gemini": config.COOLDOWN_GEMINI,
        "vision": config.COOLDOWN_VISION,
        "translate": config.COOLDOWN_TRANSLATE,
        "summarize": config.COOLDOWN_SUMMARIZE,
        "code": config.COOLDOWN_CODE,
        "imagine": config.COOLDOWN_IMAGINE,
    }

    for cmd_name, cooldown_time in commands_cooldowns.items():
        remaining = cooldown_manager.get_remaining_cooldown(cmd_name, user_id, cooldown_time)
        if remaining > 0:
            status = f"⏳ {remaining:.1f}s remaining"
        else:
            status = "✅ Ready"

        embed.add_field(name=f"!{cmd_name}", value=status, inline=True)

    await ctx.send(embed=embed)

@bot.command(name="help", aliases=["commands", "info"])
async def help_command(ctx):
    """Display list of available commands."""
    help_embed = discord.Embed(
        title="🤖 Gemini AI Discord Bot Help",
        description="Use these commands to interact with Gemini AI.",
        color=discord.Color.blue()
    )

    # Basic Commands
    help_embed.add_field(
        name="📝 Basic Commands",
        value=(
            f"`{config.COMMAND_PREFIX}gemini [question]` - Chat with Gemini AI\n"
            f"`{config.COMMAND_PREFIX}vision [description]` - Analyze images\n"
            f"`{config.COMMAND_PREFIX}reset` - Reset conversation history\n"
            f"`{config.COMMAND_PREFIX}cooldown_status` - Check cooldown status"
        ),
        inline=False
    )

    # Advanced Commands (from cogs)
    help_embed.add_field(
        name="⚡ Advanced Commands",
        value=(
            f"`{config.COMMAND_PREFIX}translate [language] [text]` - Translate text\n"
            f"`{config.COMMAND_PREFIX}summarize [text]` - Summarize content\n"
            f"`{config.COMMAND_PREFIX}code [language] [description]` - Generate code\n"
            f"`{config.COMMAND_PREFIX}imagine [description]` - Optimize image prompts"
        ),
        inline=False
    )

    # Admin Commands
    if PermissionManager.is_admin(ctx.author):
        help_embed.add_field(
            name="🔧 Admin Commands",
            value=(
                f"`{config.COMMAND_PREFIX}temperature [value]` - Set AI temperature\n"
                f"`{config.COMMAND_PREFIX}stats` - Show bot statistics\n"
                f"`{config.COMMAND_PREFIX}reset_all` - Reset all conversations"
            ),
            inline=False
        )

    help_embed.add_field(
        name="ℹ️ Information",
        value=(
            "• Commands have cooldowns to prevent spam\n"
            "• Admins bypass cooldowns and rate limits\n"
            "• Use `!cooldown_status` to check your cooldowns"
        ),
        inline=False
    )

    help_embed.set_footer(text="Gemini AI Discord Bot | Powered by Google Gemini")

    await ctx.send(embed=help_embed)

if __name__ == "__main__":
    if not config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN is not set. Please check your .env file.")
    elif not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set. Please check your .env file.")
    else:
        bot.run(config.DISCORD_TOKEN)
