import logging, os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
from urllib.parse import quote_plus

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# URL encode MongoDB connection details
USERNAME = quote_plus('<username>')
PASSWORD = quote_plus('<password>')
CLUSTER = 'cluster0'

# Construct MongoDB URI
MONGODB_URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER}.t2nvriq.mongodb.net/?retryWrites=true&w=majority"

# Initialize MongoDB connection
mongo = MongoClient(MONGODB_URI)
db = mongo.db
collection = db['papers']

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Welcome to the Question Paper Bot.\n\n'
                              'Please select your branch:', reply_markup=branch_keyboard())

# Define a function to handle the /year command
def year(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You typed /year')

# Define a function to handle the /branch command
def branch(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('You typed /branch')

# Function to create keyboard with branch options
def branch_keyboard():
    # Define the options for branch selection
    branches = ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering"]
    keyboard = [[branch] for branch in branches]

    # Return ReplyKeyboardMarkup object
    return {'keyboard': keyboard, 'one_time_keyboard': True}

# Define a function to handle text messages
def handle_text(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if "branch" not in context.user_data:
        context.user_data["branch"] = message
        update.message.reply_text("Great! Now, please provide your year.")
    elif "year" not in context.user_data:
        try:
            year = int(message)
            context.user_data["year"] = year
            update.message.reply_text("Awesome! Lastly, please provide the subject.")
        except ValueError:
            update.message.reply_text("Please provide a valid year (e.g., 1 for 1st Year).")
    elif "subject" not in context.user_data:
        context.user_data["subject"] = message
        branch = context.user_data["branch"]
        year = context.user_data["year"]
        subject = context.user_data["subject"]

        # Query MongoDB for question paper based on branch, year, and subject
        question_paper = mongo.find_question_paper(branch, year, subject)

        if question_paper:
            update.message.reply_document(document=question_paper)
        else:
            update.message.reply_text("Sorry, we couldn't find the question paper. Please try again later.")

        # Clear user data
        del context.user_data["branch"]
        del context.user_data["year"]
        del context.user_data["subject"]
    else:
        update.message.reply_text("You have already provided all the required information.")

def main(token: str) -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("year", year))
    dispatcher.add_handler(CommandHandler("branch", branch))

    # Register message handler for text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

# Execute main function when the script is executed
if __name__ == '__main__':
    # Replace 'YOUR_TOKEN' with your actual bot token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token is None:
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable.")
    else:
        main(token)
