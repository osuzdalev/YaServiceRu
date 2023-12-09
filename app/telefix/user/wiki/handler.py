import os
import pathlib
from typing import Dict

from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from app.telefix.common.types import TgHandlerPriority, TgModuleType
from .constants import (
    STATE,
    BROWSER_HISTORY_NAME,
    ENTRY_PAGE_NAME,
    ENTRY_PAGE_TEXT,
    ENTRY_PAGE_MESSAGES,
    ENTRY_PAGE_KEYBOARD,
)

from .telegram_website import Website, Page
from .wiki import wiki, wiki_callback, cancel_command


class WikiHandler:
    """
    Manages the interaction flow for a Wiki-like feature in a Telegram bot.

    This class is responsible for setting up and handling the Wiki feature, which includes
    creating a website-like experience using the `Website` and `Page` classes, handling
    conversation states, and managing entry and fallback commands. The Wiki feature is
    designed to provide users with an interactive guide or reference within the Telegram bot.

    Attributes:
        folder_path (str): Path to the folder containing the Wiki's YAML configuration files.
        commands (list of str): Commands associated with the Wiki feature.
        messages (list of str): Trigger messages for the Wiki feature.
        conversation_handler (ConversationHandler): Manages the conversation flow of the Wiki feature.

    Methods:
        get_handlers(): Returns the conversation handler for the Wiki feature.

    The WikiHandler class utilizes the Telegram bot's ConversationHandler to manage the
    interaction states and relies on the `Website` and `Page` classes to create a navigable
    Wiki structure. It uses YAML files to define the layout and content of the Wiki pages.
    """

    TYPE = TgModuleType.WIKI
    COMMANDS = ["wiki", "cancel"]
    MESSAGES = ["📖Справочник", "❌Отменить"]

    def __init__(self, wiki_data_dict: Dict, media_path: pathlib):
        # Generating the telegram_website object from yaml database file
        website = Website(STATE, BROWSER_HISTORY_NAME, media_path)
        # Parse the yaml file
        website.parse(wiki_data_dict)
        # Adding the first page to website
        entry_page = Page(
            ENTRY_PAGE_NAME,
            ENTRY_PAGE_TEXT,
            ENTRY_PAGE_MESSAGES,
            ENTRY_PAGE_KEYBOARD,
            None,
            STATE,
            BROWSER_HISTORY_NAME,
        )
        website.add_page(ENTRY_PAGE_NAME, entry_page, wiki_callback)

        self.conversation_handler = ConversationHandler(
            entry_points=[
                CommandHandler(self.COMMANDS[0], wiki),
                MessageHandler(filters.Regex(rf"^({self.MESSAGES[0]})$"), wiki),
            ],
            states=website.state,
            fallbacks=[
                CommandHandler(self.COMMANDS[1], cancel_command),
                MessageHandler(
                    filters.Regex(rf"^({self.MESSAGES[1]})$"), cancel_command
                ),
            ],
            allow_reentry=True,
            conversation_timeout=15,
        )

    def get_handlers(self):
        return {
            TgHandlerPriority.CLIENT_WIKI: [self.conversation_handler],
        }
