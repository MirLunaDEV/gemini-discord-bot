import logging
import config
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('gemini-discord-bot')

def main():
    """Main function to run the bot"""
    if not config.DISCORD_TOKEN:
        logger.error("DISCORD_TOKEN is not set. Please check your .env file.")
        return

    if not config.GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY is not set. Please check your .env file.")
        return

    try:
        import bot
        logger.info("Starting bot...")
        bot.bot.run(config.DISCORD_TOKEN)
    except Exception as e:
        logger.error(f"Error running bot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
