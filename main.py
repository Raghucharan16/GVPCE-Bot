import telegram
from bot import dispatcher
from config import TOKEN

# Create the bot instance
bot = telegram.Bot(token=TOKEN)

# Start the bot
dispatcher.start(bot)

# Keep the bot running
dispatcher.idle()
