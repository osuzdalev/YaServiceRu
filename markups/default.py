from telegram import ReplyKeyboardMarkup, KeyboardButton

keyboard = [
    [KeyboardButton("📖Вики"), KeyboardButton("🤖YaService-GPT")],
    [KeyboardButton("🤓Специалист"), KeyboardButton("❌Отменить")]
]
default_client_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
