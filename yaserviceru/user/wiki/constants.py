from telegram import InlineKeyboardButton, InlineKeyboardMarkup

DATA_PATH = "../../../data/user/wiki/data.yaml"

CANCEL = "❌ЗАКРЫТЬ"
BACK = "<< НАЗАД"

STATE = "WIKI"
BROWSER_HISTORY_NAME = "WIKI_HISTORY"
ENTRY_PAGE_NAME = "Wiki"
ENTRY_PAGE_TEXT = "Выберите ОС"
ENTRY_PAGE_MESSAGES = {}
ENTRY_PAGE_KEYBOARD = [
    [
        InlineKeyboardButton(text="Apple", callback_data="Apple"),
        InlineKeyboardButton(text="Windows", callback_data="Windows"),
    ],
    [InlineKeyboardButton(text=CANCEL, callback_data=CANCEL)],
]
ENTRY_PAGE_MARKUP = InlineKeyboardMarkup(ENTRY_PAGE_KEYBOARD)
