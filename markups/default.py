from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton("📖Вики"), KeyboardButton("🤓Специалист")],
    [KeyboardButton("❌Отменить")]
]
default_client_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
