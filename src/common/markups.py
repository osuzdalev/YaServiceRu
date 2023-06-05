from telegram import ReplyKeyboardMarkup, KeyboardButton

__keyboard = [
    [KeyboardButton("📖Справочник"), KeyboardButton("🤖Чат с подержкой")],
    [KeyboardButton("🤓Специалист")],
]
DEFAULT_CLIENT_MARKUP = ReplyKeyboardMarkup(__keyboard, resize_keyboard=True)
