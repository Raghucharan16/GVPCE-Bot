import telegram
from telegram import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    # ... (same as before)

def get_departments_keyboard():
    # Generate keyboard with department options
    departments = ["Department 1", "Department 2", "Department 3"]  # Replace with actual departments
    keyboard = [
        [KeyboardButton(department)] for department in departments
    ]
    return ReplyKeyboardMarkup(keyboard)

def get_years_keyboard():
    # Generate keyboard with year options
    years = [2020, 2021, 2022, 2023]  # Replace with relevant years
    keyboard = [
        [KeyboardButton(str(year))] for year in years
    ]
    return ReplyKeyboardMarkup(keyboard)

# ... Define other keyboards as needed

