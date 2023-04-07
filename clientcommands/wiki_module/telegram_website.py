import re
import logging
from typing import List
import copy
import yaml
import os
import pprint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, LabeledPrice
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)

from resources.constants_loader import load_constants
constants = load_constants()

logger_website = logging.getLogger(__name__)

BACK = "<< НАЗАД"
CANCEL = "OTMEНИТЬ"

class Loader(yaml.SafeLoader):
    """Special class that enables parsing the '!include' tag in the yaml files"""
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, Loader)


Loader.add_constructor('!include', Loader.include)


class Page:
    def __init__(self, name: str, text: str, messages: dict, keyboard: List[List]):
        self.name = name
        self.text = text
        self.messages = messages
        self.keyboard = keyboard


class Website:
    def __init__(self, state_name: str, browser_history_name: str):
        self.browser_history_name = browser_history_name
        self.state_name = state_name
        self.pages = {}
        self.state = {self.state_name: []}

    def format_title(self, title: str) -> str:
        return "__*" + title + "*__"

    def parse(self, config_file):
        """ Parses a YAML file and generates the pages of the website from the data
        Format of Page
        text: Text to be displayed on the page

        buttons:
        - - - Button_1_text
           - Button_1_callback_data
         - - Button_2_text
           - Button_2_callback_data
        - - - Button_3_text
           - Button_3_callback_data
         - - Button_4_text
           - Button_4_callback_data
        ..."""
        with open(config_file, mode="rb") as fp:
            config = yaml.load(fp, Loader=Loader)

        # Generates the pages from the yaml file
        for name, info in config.items():
            back_button = InlineKeyboardButton(text=BACK, callback_data="BACK")
            cancel_button = InlineKeyboardButton(text=CANCEL, callback_data="CANCEL")
            # Check if there are buttons on the page and parse them accordingly
            try:
                buttons = info['buttons']
                keyboard = [[InlineKeyboardButton(text=buttons[i][j][0], callback_data=buttons[i][j][1]) for j in
                             range(len(buttons[i]))] for i in range(len(buttons))]
            except KeyError:
                keyboard = []
            # Standardise the page for navigation by adding the CANCEL and BACK buttons at the end
            keyboard.append([back_button, cancel_button])

            # Check if there are annex messages to be sent with the page
            try:
                messages = info["messages"]
            except KeyError:
                messages = {}

            # Make title bold for Markdown V2
            title = self.format_title(info["text"])

            self.pages[name] = Page(name, title, messages, keyboard)

            # NOTE: NEEDED OTHERWISE DOES NOT WORK BECAUSE PYTHON...
            page = copy.deepcopy(self.pages[name])

            # Check if page has an Invoice option and generate the invoice handler callback accordingly
            try:
                invoice = copy.deepcopy(info["invoice"])

                async def invoice_handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, page=page, invoice=invoice) -> None:
                    """Sends an invoice without shipping-payment."""
                    query = update.callback_query
                    user = query.from_user
                    logger_website.info("({}, {}, {}) /cancel_request".format(user.id, user.name, user.first_name))
                    await query.answer()

                    logger_website.debug("This is the invoice_handler_callback for the page {}".format(page.name))
                    logger_website.debug("My buttons are: {}".format(page.keyboard))

                    chat_id = update.effective_chat.id
                    title = invoice["title"]
                    description = invoice["description"]
                    # select a payload just for you to recognize its the donation from your bot
                    payload = invoice["payload"]
                    currency = invoice["currency"]
                    price = invoice["price"]
                    label = invoice["label"]
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
                        chat_id, title, description, payload, constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA_TEST"),
                        currency, prices
                    )

                # Add the handler callback to the state
                self.state[self.state_name].append(CallbackQueryHandler(invoice_handler_callback, pattern=invoice["callback_pattern"]))
            except KeyError:
                pass

            # Generates the "Navigation" handler callback for the page

            async def handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, page=page) -> str:
                query = update.callback_query
                await query.answer()

                logger_website.debug("This is the handler callback for the page {}".format(page.name))
                logger_website.debug("I'm listening to the callback_data {}".format(update.callback_query.data))
                logger_website.debug("My buttons are: {}".format(page.keyboard))

                # Save the current page in browsing history
                browser_history = context.user_data[self.browser_history_name]
                browser_history.append(page.name)
                logger_website.debug(browser_history)

                # Save the context for request message to expert
                pattern = r'[_*]+'
                output_text = re.sub(pattern, '', page.text)
                context.user_data["Device_Context"].append(output_text)

                # Checking if there are annex messages to be sent also
                if page.messages:
                    for key in page.messages:
                        if page.messages[key][0] == "text":
                            message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                                           text=page.messages[key][1], parse_mode=ParseMode.MARKDOWN_V2)
                            context.user_data["Annexe_Messages"].append(message)
                        elif page.messages[key][0] == "picture":
                            message = await context.bot.send_photo(chat_id=update.effective_chat.id,
                                                         photo=page.messages[key][1], parse_mode=ParseMode.MARKDOWN_V2)
                            context.user_data["Annexe_Messages"].append(message)

                await query.edit_message_text(text=page.text,
                                              reply_markup=InlineKeyboardMarkup(page.keyboard),
                                              parse_mode=ParseMode.MARKDOWN_V2)

                return self.state_name
            # Add the handler callback to the state
            self.state[self.state_name].append(CallbackQueryHandler(handler_callback, pattern=page.name))

    def set_standard_handler_callbacks(self):
        """Add the "BACK" and "CANCEL" functionality as well"""

        async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            logger_website.info("cancel_callback()")
            query = update.callback_query
            await query.answer()
            await query.delete_message()
            context.user_data["in_conversation"] = ""
            return ConversationHandler.END

        self.state[self.state_name].append(CallbackQueryHandler(cancel_callback, pattern="CANCEL"))

        async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
            """
            A callback function implementing the '<- go back' back arrow equivalent in internet browsers.
            Catches the 'BACK' callback data, determines what was the previous page message the client was on,
            and calls the appropriate callback function. Updates the browsing history accordingly.
            """
            logger_website.info("back_callback()")

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
            await query.edit_message_text(text=self.pages[target_handler_callback].text,
                                          reply_markup=InlineKeyboardMarkup(self.pages[target_handler_callback].keyboard),
                                          parse_mode=ParseMode.MARKDOWN)

            return self.state_name

        self.state[self.state_name].append(CallbackQueryHandler(back_callback, pattern="BACK"))

    def add_page(self, page_name, page, callback):
        self.pages[page_name] = page
        self.state[self.state_name].append(CallbackQueryHandler(callback, pattern=page_name))
