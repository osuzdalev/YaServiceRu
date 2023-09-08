from telegram import InlineKeyboardButton


DATA_PATH = "../../../../data/command/wiki/wiki_data.yaml"

CANCEL = "❌ЗАКРЫТЬ"

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
