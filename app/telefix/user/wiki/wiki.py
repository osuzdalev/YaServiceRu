import inspect
import logging
from typing import Union

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from .constants import (
    ENTRY_PAGE_MARKUP,
    BROWSER_HISTORY_NAME,
    ENTRY_PAGE_NAME,
    ENTRY_PAGE_TEXT,
    STATE,
)

logger_wiki = logging.getLogger(__name__)


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[str, int]:
    """Customer user: Opens an Inline Menu to search for some information. As Buttons are pressed and going
    through the decision tree, the user_data 'device_context' is updated.
    This Conversation first needs to check the user 'in_conversation flag' before it can start, otherwise it will ask
    the customer to first close the previous one."""
    user = update.message.from_user
    logger_wiki.info(
        f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
    )
    # Context history for the user's session
    context.user_data["Device_Context"] = []
    context.user_data["Annexe_Messages"] = []

    # Create a browser history for the user's session
    context.user_data[BROWSER_HISTORY_NAME] = [ENTRY_PAGE_NAME]

    # Check if user already in Conversation
    in_conversation = context.user_data.get("in_conversation", "")
    if not (in_conversation == "" or in_conversation == "wiki"):
        await update.message.reply_text(
            "Please press /cancel\n"
            "or push the 'CANCEL' button in the previous menu before proceeding"
        )
        return ConversationHandler.END
    context.user_data["in_conversation"] = "wiki"

    await update.message.reply_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def wiki_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """A callback function which has the same output as the wiki user. Necessary if the user wants to browse back
    to the first page of the wiki"""
    user = update.message.from_user
    logger_wiki.info(
        f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
    )
    context.user_data[BROWSER_HISTORY_NAME].append(ENTRY_PAGE_NAME)

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(ENTRY_PAGE_TEXT, reply_markup=ENTRY_PAGE_MARKUP)

    return STATE


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger_wiki.info(
        f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
    )
    context.user_data["in_conversation"] = ""
    context.user_data["Annexe_Messages"] = []
    return ConversationHandler.END
