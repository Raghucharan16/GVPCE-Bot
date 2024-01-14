import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from keyboards import get_main_keyboard, get_departments_keyboard, get_years_keyboard

# Define conversation states
CHOOSING_DEPARTMENT, CHOOSING_YEAR, CHOOSING_SUBJECT = range(3)

# Handler for initial message
def start(update, context):
    context.user_data.clear()
    update.message.reply_text("Welcome to the Question Papers Bot!", reply_markup=get_main_keyboard())
    return CHOOSING_DEPARTMENT

# Handler for choosing department
def handle_choosing_department(update, context):
    chosen_department = update.message.text
    context.user_data['department'] = chosen_department
    update.message.reply_text("Great! Now choose the year:", reply_markup=get_years_keyboard())
    return CHOOSING_YEAR

# Handler for choosing year
def handle_choosing_year(update, context):
    chosen_year = update.message.text
    department = context.user_data['department']

    # Connect to MongoDB
    client = MongoClient(DATABASE_UR)
    db = client['question_papers']
    papers_collection = db['papers']

    # Query for subjects based on department and year
    subjects = papers_collection.distinct('subject', {'department': department, 'year': chosen_year})

    # Create keyboard with subject options
    subjects_keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(subject)] for subject in subjects
    ])

    update.message.reply_text("Choose a subject:", reply_markup=subjects_keyboard)
    context.user_data['year'] = chosen_year  # Store year string for later use
    return CHOOSING_SUBJECT

# Handler for choosing subject
def handle_choosing_subject(update, context):
    chosen_subject = update.message.text
    department = context.user_data['department']
    year = context.user_data['year']

    # Fetch papers based on department, year, and subject
    papers = papers_collection.find({'department': department, 'year': year, 'subject': chosen_subject})

    # Display paper titles and download links
    paper_buttons = []
    for paper in papers:
        # Assuming you store file URLs in 'pdf_url' field
        paper_button = InlineKeyboardButton(paper['title'], url=paper['pdf_url'])
        paper_buttons.append([paper_button])

    reply_markup = InlineKeyboardMarkup(paper_buttons)
    update.message.reply_text("Here are the available papers:", reply_markup=reply_markup)

# Handler for downloading paper
def send_paper(update, context):
    query = update.callback_query
    paper_url = query.data  # Extract paper URL from callback query data

    # Using telepot for sending document 
    bot = telepot.Bot(BOT_TOKEN)
    bot.sendDocument(query.message.chat.id, document=paper_url)

# Fallback handler for unexpected input
def handle_fallback(update, context):
    update.message.reply_text("Sorry, I didn't understand that. Please try again or use the /start command.")

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(ConversationHandler(
    entry_points=[MessageHandler(Filters.text & ~Filters.command, start)],
    states={
        CHOOSING_DEPARTMENT: [MessageHandler(Filters.text, handle_choosing_department)],
        CHOOSING_YEAR: [MessageHandler(Filters.text & Filters.regex(r'^\d{4}$'), handle_choosing_year)],
        CHOOSING_SUBJECT: [MessageHandler(Filters.text, handle_choosing_subject)],
    },
    fallbacks=[MessageHandler(Filters.text & ~Filters.command, handle_fallback)],
))
dispatcher.add_handler(CallbackQueryHandler(send_paper))
