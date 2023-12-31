import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo
import urllib.parse
import time

# Placeholders - Replace with your actual values
YOUR_DATABASE_URL = "mongodb://your_username:your_password@your_database_host:your_database_port/your_database_name"
YOUR_BOT_TOKEN = "123456789:YourActualBotToken"

# Escape username and password for MongoDB connection
username = urllib.parse.quote_plus("your_username")
password = urllib.parse.quote_plus("your_password")
uri = "mongodb://" + username + ":" + password + "@" + YOUR_DATABASE_URL[10:]

# Connect to MongoDB
client = pymongo.MongoClient(uri)
db = client['question_papers']
papers_collection = db['papers']

# Telegram bot setup
bot = telepot.Bot(YOUR_BOT_TOKEN)

def handle_choosing_subject(update, context):
    departments = ['CSE', 'ECE', 'Mechanical', 'IT', 'Civil', 'Chemical', 'EEE']  # Available departments

    department_buttons = []
    for department in departments:
        department_button = InlineKeyboardButton(department, callback_data=department)
        department_buttons.append([department_button])

    reply_markup = InlineKeyboardMarkup(department_buttons)
    update.message.reply_text("Choose your department:", reply_markup=reply_markup)

def handle_chosen_department(update, context):
    chosen_department = update.callback_query.data
    context.user_data['department'] = chosen_department

    # ... (Rest of your code to get papers based on department and continue the flow)

def send_paper(update, context):
    # ... (Code to send the paper as before)

# Start the bot and handle messages
MessageLoop(bot, {'chat': handle_choosing_subject,
                   'callback_query': handle_chosen_department,  # Handle department choice
                   'callback_query': send_paper}).run_as_thread()

print('Bot is listening ...')

# Keep the program running (add other functionalities here as needed)
while 1:
    time.sleep(10)
