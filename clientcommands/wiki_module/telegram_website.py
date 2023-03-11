import logging
from typing import List
import copy
import yaml
import os
import pprint

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)

logger_website = logging.getLogger(__name__)


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
    def __init__(self, name: str, text: str, keyboard: List[List]):
        self.name = name
        self.text = text
        self.keyboard = keyboard


class Website:
    def __init__(self, state_name: str, browser_history_name: str):
        self.browser_history_name = browser_history_name
        self.state_name = state_name
        self.pages = {}
        self.state = {self.state_name: []}

    def parse(self, config_file):
        """ Parses a YAML and generates the pages of the website from the data"""
        # Generates the pages from the yaml file
        with open(config_file, mode="rb") as fp:
            config = yaml.load(fp, Loader=Loader)

        for name, info in config.items():
            back_button = InlineKeyboardButton(text="<< BACK", callback_data="BACK")
            cancel_button = InlineKeyboardButton(text="CANCEL", callback_data="CANCEL")
            # Check if there are buttons on the page and parse them accordingly
            try:
                buttons = info['buttons']
                keyboard = []
                for i in range(len(buttons)):
                    button_row = []
                    for j in range(len(buttons[i])):
                        button = InlineKeyboardButton(text=buttons[i][j][0], callback_data=buttons[i][j][1])
                        button_row.append(button)
                    keyboard.append(button_row)
                # Standardise the page for navigation by adding the CANCEL and BACK buttons at the end
                keyboard.append([back_button, cancel_button])
            except KeyError:
                keyboard = [[back_button, cancel_button]]

            self.pages[name] = Page(name, info["text"], keyboard)

        # Generates the handler callback for each page
        for page in self.pages:
            if page == "<< BACK" or page == "CANCEL":
                pass
            else:
                page_name = copy.deepcopy(page)

                async def handler_callback(update: Update, context: ContextTypes.DEFAULT_TYPE,
                                           page_name=page_name) -> str:

                    query = update.callback_query
                    await query.answer()

                    logger_website.debug("This is the handler callback for the page {}".format(page_name))
                    logger_website.debug("I'm listening to the callback_data {}".format(update.callback_query.data))
                    logger_website.debug("My buttons are: {}".format(self.pages[page_name].keyboard))

                    # Save the current page in browsing history
                    browser_history = update.effective_user.id
                    if self.browser_history_name in context.user_data:
                        browser_history = context.user_data[self.browser_history_name]
                    browser_history.append(page_name)
                    logger_website.debug(browser_history)

                    await query.edit_message_text(text=self.pages[page_name].text,
                                                  reply_markup=InlineKeyboardMarkup(self.pages[page_name].keyboard),
                                                  parse_mode=ParseMode.MARKDOWN)

                    return self.state_name

                self.state[self.state_name].append(
                    CallbackQueryHandler(copy.deepcopy(handler_callback), pattern=page_name))

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
            logger_website.debug(browser_history)
            # Determine where clients wants to go
            target_handler_callback = browser_history[-1]
            # Generate appropriate response
            # TODO
            await query.edit_message_text(text=self.pages[target_handler_callback].text,
                                          reply_markup=InlineKeyboardMarkup(self.pages[target_handler_callback].keyboard),
                                          parse_mode=ParseMode.MARKDOWN)

            return self.state_name

        self.state[self.state_name].append(CallbackQueryHandler(back_callback, pattern="BACK"))

    def add_page(self, page_name, page, callback):
        self.pages[page_name] = page
        self.state[self.state_name].append(CallbackQueryHandler(callback, pattern=page_name))

    def add_callback_query_handler(self, callback_function, callback_data):
        """Add a partial CallbackQueryHandler to the handlers dict of the website"""
        self.state[self.state_name].append(CallbackQueryHandler(callback_function, callback_data))
