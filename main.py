from dotenv import load_dotenv
import os
from bot.bot import main as start_bot

# Load environment variables from .env file
load_dotenv()

# Get Telegram bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    if TOKEN is None:
        print("Please provide the Telegram bot token in the .env file.")
        return

    start_bot(TOKEN)

if __name__ == "__main__":
    main()
