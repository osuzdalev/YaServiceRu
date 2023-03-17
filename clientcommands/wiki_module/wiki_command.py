import logging
from typing import Union
import os
import pprint

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

from clientcommands.wiki_module.telegram_website import Website, Page

logger_wiki = logging.getLogger(__name__)

DATA_PATH = "wiki_data/wiki_data.yaml"
FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_PATH)

BACK = "BACK"
CANCEL = "CANCEL"

STATE = "WIKI"
BROWSER_HISTORY_NAME = "WIKI_HISTORY"
ENTRY_PAGE_NAME = "Wiki"
ENTRY_PAGE_TEXT = "Select a Brand/OS"
ENTRY_PAGE_MESSAGES = {}
ENTRY_PAGE_KEYBOARD = [
    [InlineKeyboardButton(text="Apple", callback_data="Apple"),
     InlineKeyboardButton(text="Windows", callback_data="Windows")],
    [InlineKeyboardButton(text=CANCEL, callback_data=CANCEL)]
]
ENTRY_PAGE_MARKUP = InlineKeyboardMarkup(ENTRY_PAGE_KEYBOARD)
entry_page = Page(ENTRY_PAGE_NAME, ENTRY_PAGE_TEXT, ENTRY_PAGE_MESSAGES, ENTRY_PAGE_KEYBOARD)


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[str, int]:
    """Customer command: Opens an Inline Menu to search for some information. As Buttons are pressed and going
    through the decision tree, the user_data 'device_context' is updated.
    This Conversation first needs to check the user 'in_conversation flag' before it can start, otherwise it will ask
    the customer to first close the previous one."""
    logger_wiki.info("wiki_module()")
    # Context history for the user's session
    device_context = {"OS": '', "Device": '', "Category": '', "Problem": ''}
    context.user_data["Device_Context"] = device_context
    context.user_data["Annexe_Messages"] = []

    # Create a browser history for the user's session
    context.user_data[BROWSER_HISTORY_NAME] = [ENTRY_PAGE_NAME]

    try:
        in_conversation = context.user_data['in_conversation']
    except KeyError:
        raise KeyError("Command '/start' not yet used by User.")

    # Check if user already in Conversation
    if not (in_conversation == '' or in_conversation == 'wiki_module'):
        await update.message.reply_text("Please press /cancel\n"
                                        "or push the 'CANCEL' button in the previous menu before proceeding")
        return ConversationHandler.END
    context.user_data["in_conversation"] = "wiki_module"

    await update.message.reply_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def wiki_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """A callback function which has the same output as the wiki command. Necessary if the client wants to browse back
    to the first page of the wiki"""
    logger_wiki.info("wiki_module()")
    context.user_data[BROWSER_HISTORY_NAME].append(ENTRY_PAGE_NAME)

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def cancel_command(_: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger_wiki.info("cancel_command()")
    context.user_data["in_conversation"] = ""
    context.user_data["Annexe_Messages"] = []
    return ConversationHandler.END

# Generating the telegram_website object from yaml data file
website = Website(STATE, BROWSER_HISTORY_NAME)
# TODO Can this be done at init()?
website.set_standard_handler_callbacks()
# Parse the yaml file
website.parse(FULL_PATH)
# Adding the first page to website
website.add_page(ENTRY_PAGE_NAME, entry_page, wiki_callback)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("wiki", wiki), MessageHandler(filters.Regex(r"^(📖Вики)$"), wiki)],
    states=website.state,
    fallbacks=[CommandHandler("cancel", cancel_command),
               MessageHandler(filters.Regex(r"^(❌Отменить)$"), cancel_command)],
    allow_reentry=True,
    conversation_timeout=15
)
