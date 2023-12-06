import pathlib

from loguru import logger
from typing import Dict

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler

from .constants import BACK, CANCEL
from .page import Page


class Website:
    """
    Manages a collection of `Page` objects to simulate a website-like navigation experience in a Telegram bot.

    This class is responsible for parsing configuration files to generate pages, handling navigation
    between these pages, and managing state transitions within the bot's conversation handler.

    Attributes:
        browser_history_name (str): Key name for storing browsing history in user context.
        state_name (str): The name of the state associated with the website in the conversation handler.
        pages (dict): Dictionary of `Page` objects representing the pages of the website.
        state (dict): State configuration for the conversation handler.

    Methods:
        format_title(title): Formats the title string for display.
        parse(config_file): Parses a YAML configuration file to generate the website's pages.
        cancel_callback(update, context): Handles the cancellation of the navigation.
        add_cancel_callback(): Adds the cancel callback to the state handlers.
        back_callback(update, context): Handles the back navigation within the website.
        add_back_callback(): Adds the back callback to the state handlers.
        add_page(page_name, page, callback): Adds a new page to the website.
    """

    def __init__(self, state_name: str, browser_history_name: str, media_dir: pathlib):
        self.state_name = state_name
        self.browser_history_name = browser_history_name
        self.media_dir = media_dir
        self.pages = {}
        self.state = {self.state_name: []}
        self.add_back_callback()
        self.add_cancel_callback()

    def format_title(self, title: str) -> str:
        return f"__*{title}*__"

    def parse(self, wiki_data_dict: Dict):
        """Generates the pages of the website from the provided configuration dictionary"""

        # Generates the pages from the yaml file
        for name, info in wiki_data_dict.items():
            back_button = InlineKeyboardButton(text=BACK, callback_data=BACK)
            cancel_button = InlineKeyboardButton(text=CANCEL, callback_data=CANCEL)
            # Check if there are buttons on the page and parse them accordingly
            if "buttons" in info:
                buttons = info["buttons"]
                keyboard = [
                    [
                        InlineKeyboardButton(
                            text=buttons[i][j][0], callback_data=buttons[i][j][1]
                        )
                        for j in range(len(buttons[i]))
                    ]
                    for i in range(len(buttons))
                ]
            else:
                keyboard = []
            # Standardise the page for navigation by adding the CANCEL and BACK buttons at the end
            keyboard.append([back_button, cancel_button])

            # Check if there are annex messages to be sent with the page
            messages = info.get("messages") or {}

            # Make title bold for Markdown V2
            title = self.format_title(info["title"])

            self.pages[name] = Page(
                name,
                title,
                messages,
                keyboard,
                info.get("invoice"),
                self.state_name,
                self.browser_history_name,
                self.media_dir,
            )

            self.state[self.state_name].extend(self.pages[name].handlers)

    async def cancel_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        user = update.effective_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

        query = update.callback_query
        await query.answer()
        await query.delete_message()
        context.user_data["in_conversation"] = ""
        return ConversationHandler.END

    def add_cancel_callback(self):
        self.state[self.state_name].append(
            CallbackQueryHandler(self.cancel_callback, pattern=CANCEL)
        )

    async def back_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        """
        A callback function implementing the '<- go back' back arrow equivalent in internet browsers.
        Catches the 'BACK' callback data, determines what was the previous page message the user was on,
        and calls the appropriate callback function. Updates the browsing history accordingly.
        """
        user = update.effective_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

        query = update.callback_query
        await query.answer()

        # Get the last visited page from browsing history
        browser_history = context.user_data[self.browser_history_name]
        # Delete previous page in history
        browser_history.pop()
        context.user_data["Device_Context"].pop()
        logger.debug(browser_history)
        # Determine where clients wants to go
        target_handler_callback = browser_history[-1]
        # Delete the messages from the answer to avoid clutter
        for message in context.user_data["Annexe_Messages"]:
            await message.delete()
        context.user_data["Annexe_Messages"] = []
        # Generate appropriate response
        await query.edit_message_text(
            text=self.pages[target_handler_callback].title,
            reply_markup=InlineKeyboardMarkup(
                self.pages[target_handler_callback].keyboard
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

        return self.state_name

    def add_back_callback(self):
        self.state[self.state_name].append(
            CallbackQueryHandler(self.back_callback, pattern=BACK)
        )

    def add_page(self, page_name, page, callback):
        self.pages[page_name] = page
        self.state[self.state_name].append(
            CallbackQueryHandler(callback, pattern=page_name)
        )
