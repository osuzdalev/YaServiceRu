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
from src.command.client.wiki.config import *
from src.common.types import HandlerGroupType

FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_PATH)
entry_page = Page(
    ENTRY_PAGE_NAME, ENTRY_PAGE_TEXT, ENTRY_PAGE_MESSAGES, ENTRY_PAGE_KEYBOARD
)


class WikiHandler:
    def __init__(self):
        # Generating the telegram_website object from yaml database file
        website = Website(STATE, BROWSER_HISTORY_NAME)
        # TODO Can this be done at init()?
        website.set_standard_handler_callbacks()
        # Parse the yaml file
        website.parse(FULL_PATH)
        # Adding the first page to website
        website.add_page(ENTRY_PAGE_NAME, entry_page, wiki_callback)

        self.conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler("wiki", wiki),
                MessageHandler(filters.Regex(r"^(📖Справочник)$"), wiki),
            ],
            states=website.state,
            fallbacks=[
                CommandHandler("cancel", cancel_command),
                MessageHandler(filters.Regex(r"^(❌Отменить)$"), cancel_command),
            ],
            allow_reentry=True,
            conversation_timeout=15,
        )

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_WIKI.value: [self.conversation_handler],
        }