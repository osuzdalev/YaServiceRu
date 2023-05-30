from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton("📖Справочник"), KeyboardButton("🤖Чат с подержкой")],
    [KeyboardButton("🤓Специалист")],
]
default_client_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
