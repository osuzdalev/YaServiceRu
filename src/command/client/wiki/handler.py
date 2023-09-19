import os

from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from src.command.client.wiki.wiki import (
    wiki,
    wiki_callback,
    cancel_command,
)
from src.command.client.wiki.telegram_website import Website, Page
from . import *
from src.common.types import HandlerGroupType

FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_PATH)


class WikiHandler:
    command = ["wiki", "cancel"]
    message = ["📖Справочник", "❌Отменить"]

    def __init__(self, folder_path: str, commands=None, messages=None):
        self.folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_path)
        self.commands = commands if commands else []
        self.messages = messages if messages else []

        # Generating the telegram_website object from yaml database file
        website = Website(STATE, BROWSER_HISTORY_NAME)
        # Parse the yaml file
        website.parse(FULL_PATH)
        # Adding the first page to website
        entry_page = Page(
            ENTRY_PAGE_NAME, ENTRY_PAGE_TEXT, ENTRY_PAGE_MESSAGES, ENTRY_PAGE_KEYBOARD, None, STATE,
            BROWSER_HISTORY_NAME
        )
        website.add_page(ENTRY_PAGE_NAME, entry_page, wiki_callback)

        self.conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.commands[0], wiki),
                MessageHandler(filters.Regex(fr"^({self.messages[0]})$"), wiki),
            ],
            states=website.state,
            fallbacks=[
                CommandHandler(self.commands[1], cancel_command),
                MessageHandler(filters.Regex(fr"^({self.messages[1]})$"), cancel_command),
            ],
            allow_reentry=True,
            conversation_timeout=15,
        )

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_WIKI.value: [self.conversation_handler],
        }
