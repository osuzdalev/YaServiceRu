import inspect
import re
import logging
from typing import List, Dict

import yaml

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, LabeledPrice
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler

from ...common.yaml_loader import YamlLoader
from .constants import BACK, CANCEL

logger_website = logging.getLogger(__name__)

YamlLoader.add_constructor("!include", YamlLoader.include)


class Page:
    """
    Represents a single page within a Telegram bot's interactive website-like interface.

    This class encapsulates the properties and behaviors of a page, including its name, title,
    associated messages, keyboard layout, invoice handling, and navigation functionality.

    Attributes:
        name (str): Identifier of the page.
        title (str): Title of the page, displayed at the top.
        messages (dict): Optional additional messages to be sent when the page is displayed.
        keyboard (List[List]): Keyboard layout for the page's inline buttons.
        invoice (optional): Information for handling invoice-related actions.
        return_state (optional): State to return after handling the page.
        browser_history_name (optional): Key name for storing browsing history in context.
        handlers (List): List of Telegram's CallbackQueryHandlers for the page.

    Methods:
        handler_callback(update, context): Handles callbacks triggered by the page's buttons.
        invoice_handler_callback(update, context): Handles invoice-related callbacks.
    """

    def __init__(
        self,
        name: str,
        title: str,
        messages: dict,
        keyboard: List[List],
        invoice=None,
        return_state=None,
        browser_history_name=None,
    ):
        self.name = name
        self.title = title
        self.messages = messages
        self.keyboard = keyboard
        self.invoice = invoice
        self.return_state = return_state
        self.browser_history_name = browser_history_name
        self.handlers = []

        self.handlers.append(
            CallbackQueryHandler(self.handler_callback, pattern=self.name)
        )
        if self.invoice:
            self.handlers.append(
                CallbackQueryHandler(
                    self.invoice_handler_callback,
                    pattern=self.invoice["callback_pattern"],
                )
            )

    async def handler_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        query = update.callback_query
        await query.answer()

        logger_website.debug(f"This is the handler callback for the page {self.name}")
        logger_website.debug(
            f"I'm listening to the callback_data {update.callback_query.data}"
        )
        logger_website.debug(f"My buttons are: {self.keyboard}")

        # Save the current page in browsing history
        browser_history = context.user_data[self.browser_history_name]
        browser_history.append(self.name)
        logger_website.debug(browser_history)

        # Save the context for request_module message to expert
        pattern = r"[_*]+"
        output_text = re.sub(pattern, "", self.title)
        context.user_data["Device_Context"].append(output_text)

        # Checking if there are annex messages to be sent also
        if self.messages:
            for key in self.messages:
                if self.messages[key][0] == "text":
                    message = await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=self.messages[key][1],
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                    context.user_data["Annexe_Messages"].append(message)
                elif self.messages[key][0] == "picture":
                    with open(self.messages[key][1], "rb") as photo:
                        message = await context.bot.send_photo(
                            chat_id=update.effective_chat.id, photo=photo
                        )
                    context.user_data["Annexe_Messages"].append(message)

        await query.edit_message_text(
            text=self.title,
            reply_markup=InlineKeyboardMarkup(self.keyboard),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        return self.return_state

    async def invoice_handler_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Sends an invoice without shipping-payment."""
        query = update.callback_query
        user = query.from_user
        logger_website.info(
            f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
        )
        await query.answer()

        logger_website.debug(
            f"This is the invoice_handler_callback for the page {self.page.name}"
        )
        logger_website.debug(f"My buttons are: {self.page.keyboard}")

        chat_id = update.effective_chat.id
        title = self.invoice["title"]
        description = self.invoice["description"]
        # select a payload just for you to recognize it's the donation from your bot
        payload = self.invoice["payload"]
        currency = self.invoice["currency"]
        price = self.invoice["price"]
        label = self.invoice["label"]
        # price * 100 to include 2 decimal points
        prices = [LabeledPrice(label, price * 100)]

        # Cleaning up
        await query.delete_message()
        for message in context.user_data["Annexe_Messages"]:
            await message.delete()
        context.user_data["Annexe_Messages"] = []

        # optionally pass need_name=True, need_phone_number=True,
        # need_email=True, need_shipping_address=True, is_flexible=True
        await context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            context.bot_data["config"]["telefix"]["secret"]["token_payment_provider"],
            currency,
            prices,
        )


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

    def __init__(self, state_name: str, browser_history_name: str):
        self.browser_history_name = browser_history_name
        self.state_name = state_name
        self.pages = {}
        self.state = {self.state_name: []}
        self.add_back_callback()
        self.add_cancel_callback()

    def format_title(self, title: str) -> str:
        return "__*" + title + "*__"

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
            )

            self.state[self.state_name].extend(self.pages[name].handlers)

    async def cancel_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        user = update.effective_user
        logger_website.info(
            f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
        )

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
        logger_website.info(
            f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
        )

        query = update.callback_query
        await query.answer()

        # Get the last visited page from browsing history
        browser_history = context.user_data[self.browser_history_name]
        # Delete previous page in history
        browser_history.pop()
        context.user_data["Device_Context"].pop()
        logger_website.debug(browser_history)
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
