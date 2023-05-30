import logging
from typing import Union
import os

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

from commands.client.wiki_module.telegram_website import Website, Page

logger_wiki = logging.getLogger(__name__)

DATA_PATH = "../../../data/wiki_data/wiki_data.yaml"
FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_PATH)

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
ENTRY_PAGE_MARKUP = InlineKeyboardMarkup(ENTRY_PAGE_KEYBOARD)
entry_page = Page(
    ENTRY_PAGE_NAME, ENTRY_PAGE_TEXT, ENTRY_PAGE_MESSAGES, ENTRY_PAGE_KEYBOARD
)


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[str, int]:
    """Customer command: Opens an Inline Menu to search for some information. As Buttons are pressed and going
    through the decision tree, the user_data 'device_context' is updated.
    This Conversation first needs to check the user 'in_conversation flag' before it can start, otherwise it will ask
    the customer to first close the previous one."""
    user = update.message.from_user
    logger_wiki.info("({}, {}, {}) /wiki".format(user.id, user.name, user.first_name))
    # Context history for the user's session
    context.user_data["Device_Context"] = []
    context.user_data["Annexe_Messages"] = []

    # Create a browser history for the user's session
    context.user_data[BROWSER_HISTORY_NAME] = [ENTRY_PAGE_NAME]

    # Check if user already in Conversation
    in_conversation = context.user_data.get("in_conversation", "")
    if not (in_conversation == "" or in_conversation == "wiki_module"):
        await update.message.reply_text(
            "Please press /cancel\n"
            "or push the 'CANCEL' button in the previous menu before proceeding"
        )
        return ConversationHandler.END
    context.user_data["in_conversation"] = "wiki_module"

    await update.message.reply_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def wiki_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """A callback function which has the same output as the wiki command. Necessary if the client wants to browse back
    to the first page of the wiki"""
    user = update.message.from_user
    logger_wiki.info(
        "({}, {}, {}) /wiki_callback".format(user.id, user.name, user.first_name)
    )
    context.user_data[BROWSER_HISTORY_NAME].append(ENTRY_PAGE_NAME)

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger_wiki.info(
        "({}, {}, {}) /wiki_cancel_command".format(user.id, user.name, user.first_name)
    )
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