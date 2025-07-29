import discord
from discord.ext import commands
import google.generativeai as genai
import config
import logging
from typing import Optional
import sys
import os

try:
    from utils import (
        ConversationManager, EmbedBuilder, split_long_message,
        CooldownManager, PermissionManager, InputValidator, ErrorHandler
    )
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import (
        ConversationManager, EmbedBuilder, split_long_message,
        CooldownManager, PermissionManager, InputValidator, ErrorHandler
    )

logger = logging.getLogger('gemini-discord-bot.advanced')

class AdvancedCommands(commands.Cog):
    """Advanced commands for Gemini AI features"""

    def __init__(self, bot):
        self.bot = bot
        self.conversation_manager = ConversationManager(
            max_history=config.CONVERSATION_MEMORY_LIMIT
        )
        self.cooldown_manager = CooldownManager()

        self.text_model = genai.GenerativeModel(config.GEMINI_TEXT_MODEL)
        self.pro_model = genai.GenerativeModel(config.GEMINI_PRO_MODEL)

    def check_permissions_and_cooldown(self, cooldown_time: float):
        """Decorator to check permissions and cooldowns for cog commands"""
        def decorator(func):
            async def wrapper(ctx, *args, **kwargs):
                # Check permissions
                if not PermissionManager.can_use_command(ctx.author, func.__name__):
                    await ErrorHandler.handle_permission_error(ctx, func.__name__)
                    return

                # Check cooldown (skip for admins)
                if not PermissionManager.is_admin(ctx.author):
                    if self.cooldown_manager.is_on_cooldown(func.__name__, ctx.author.id, cooldown_time):
                        remaining = self.cooldown_manager.get_remaining_cooldown(func.__name__, ctx.author.id, cooldown_time)
                        await ErrorHandler.handle_cooldown_error(ctx, remaining)
                        return

                # Set cooldown
                self.cooldown_manager.set_cooldown(func.__name__, ctx.author.id)

                # Execute command
                try:
                    await func(self, ctx, *args, **kwargs)
                except Exception as e:
                    await ErrorHandler.handle_api_error(ctx, e, "Gemini")

            return wrapper
        return decorator
    
    @commands.command(name="translate", aliases=["trans"])
    async def translate_command(self, ctx, target_language: str = None, *, text: str = None):
        """Translate text to specified language.

        Usage: !translate [target language] [text]
        Example: !translate Spanish Hello world
        """
        # Check cooldown
        if not PermissionManager.is_admin(ctx.author):
            if self.cooldown_manager.is_on_cooldown("translate_command", ctx.author.id, config.COOLDOWN_TRANSLATE):
                remaining = self.cooldown_manager.get_remaining_cooldown("translate_command", ctx.author.id, config.COOLDOWN_TRANSLATE)
                await ErrorHandler.handle_cooldown_error(ctx, remaining)
                return

        if not target_language or not text:
            await ctx.send(f"Usage: {config.COMMAND_PREFIX}translate [target language] [text]")
            return

        # Validate input
        if not InputValidator.validate_text_length(text):
            await ctx.send(f"❌ Text is too long. Maximum length: {config.MAX_MESSAGE_LENGTH} characters.")
            return

        # Sanitize input
        text = InputValidator.sanitize_input(text)
        target_language = InputValidator.sanitize_input(target_language)

        # Set cooldown
        self.cooldown_manager.set_cooldown("translate_command", ctx.author.id)

        async with ctx.typing():
            try:
                prompt = f"Translate the following text to {target_language}. Only output the translation without any explanation: {text}"

                response = self.text_model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.2,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                    }
                )

                response_text = response.text

                embed = EmbedBuilder.create_info_embed(
                    title=f"🌐 Translation to {target_language}",
                    description=response_text
                )
                embed.add_field(name="Original Text", value=text, inline=False)

                await ctx.send(embed=embed)

            except Exception as e:
                await ErrorHandler.handle_api_error(ctx, e, "Translation")
    
    @commands.command(name="summarize", aliases=["summary"])
    async def summarize_command(self, ctx, *, text: str = None):
        """Summarize text content.

        Usage: !summarize [text]
        """
        # Check cooldown
        if not PermissionManager.is_admin(ctx.author):
            if self.cooldown_manager.is_on_cooldown("summarize_command", ctx.author.id, config.COOLDOWN_SUMMARIZE):
                remaining = self.cooldown_manager.get_remaining_cooldown("summarize_command", ctx.author.id, config.COOLDOWN_SUMMARIZE)
                await ErrorHandler.handle_cooldown_error(ctx, remaining)
                return

        if not text:
            await ctx.send(f"Usage: {config.COMMAND_PREFIX}summarize [text]")
            return

        if len(text) < 100:
            await ctx.send("❌ Text is too short to summarize. Please provide at least 100 characters.")
            return

        if not InputValidator.validate_text_length(text):
            await ctx.send(f"❌ Text is too long. Maximum length: {config.MAX_MESSAGE_LENGTH} characters.")
            return

        text = InputValidator.sanitize_input(text)
        self.cooldown_manager.set_cooldown("summarize_command", ctx.author.id)

        async with ctx.typing():
            try:
                prompt = f"Summarize the following text concisely. Include only key points and important information: {text}"

                response = self.text_model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": 0.3,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 1024,
                    }
                )

                response_text = response.text

                embed = EmbedBuilder.create_info_embed(
                    title="Text Summary",
                    description=response_text
                )

                if len(text) > 1024:
                    text = text[:1021] + "..."

                embed.add_field(name="Original Text", value=text, inline=False)

                await ctx.send(embed=embed)

            except Exception as e:
                logger.error(f"Summarization error: {str(e)}")
                await ctx.send(f"An error occurred during summarization: {str(e)}")
    
    @commands.command(name="code", aliases=["generate"])
    async def code_command(self, ctx, language: str = None, *, prompt: str = None):
        """Generate code in specified programming language.

        Usage: !code [language] [description]
        Example: !code python function to calculate fibonacci sequence
        """
        if not language or not prompt:
            await ctx.send(f"Usage: {config.COMMAND_PREFIX}code [language] [description]")
            return

        async with ctx.typing():
            try:
                code_prompt = f"Write {language} code for the following description. Only output code with comments for explanation: {prompt}"

                response = self.text_model.generate_content(
                    code_prompt,
                    generation_config={
                        "temperature": 0.2,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                    }
                )

                response_text = response.text

                if not response_text.startswith("```"):
                    response_text = f"```{language}\n{response_text}\n```"

                chunks = split_long_message(response_text, config.MAX_RESPONSE_LENGTH)
                for chunk in chunks:
                    await ctx.send(chunk)

            except Exception as e:
                logger.error(f"Code generation error: {str(e)}")
                await ctx.send(f"An error occurred during code generation: {str(e)}")
    
    @commands.command(name="imagine", aliases=["prompt"])
    async def imagine_command(self, ctx, *, prompt: str = None):
        """Optimize prompts for image generation AI.

        Usage: !imagine [description]
        """
        if not prompt:
            await ctx.send(f"Usage: {config.COMMAND_PREFIX}imagine [description]")
            return

        async with ctx.typing():
            try:
                system_prompt = """
                You are a prompt optimization expert for image generation AI.
                Transform the user's simple description into detailed prompts suitable for
                image generation AI like Midjourney, DALL-E, or Stable Diffusion.

                Respond in the following format:

                **Optimized Prompt:**
                [detailed prompt]

                **Style Suggestions:**
                - [style 1]
                - [style 2]
                - [style 3]

                **Additional Keywords:**
                - [keyword 1]
                - [keyword 2]
                - [keyword 3]
                """

                user_prompt = f"Optimize the following description into a detailed prompt for image generation AI: {prompt}"

                response = self.text_model.generate_content(
                    [system_prompt, user_prompt],
                    generation_config={
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": config.MAX_OUTPUT_TOKENS,
                    }
                )

                response_text = response.text

                embed = EmbedBuilder.create_info_embed(
                    title="Image Generation Prompt",
                    description=response_text
                )

                await ctx.send(embed=embed)

            except Exception as e:
                logger.error(f"Prompt optimization error: {str(e)}")
                await ctx.send(f"An error occurred during prompt optimization: {str(e)}")

async def setup(bot):
    await bot.add_cog(AdvancedCommands(bot))
