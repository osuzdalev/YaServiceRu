import logging
from uuid import uuid4
from typing import Union

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from clientcommands.wiki_module.wiki_data import DATA_DICT

logger_wiki_share = logging.getLogger(__name__)


async def share(update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
    """Handle the inline query. This is run when you type: @OsuzOrderDispatcherBot <query>"""
    inline_query = update.inline_query.query

    if inline_query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["Problem_Title_EN"],
            input_message_content=InputTextMessageContent(
                DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["Share"]
                + DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["Text"],
                parse_mode=ParseMode.MARKDOWN),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["Problem_Title_EN"],
            input_message_content=InputTextMessageContent(
                DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["Share"]
                + DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["Text"],
                parse_mode=ParseMode.MARKDOWN),
        ),
    ]

    await update.inline_query.answer(results)
    return ConversationHandler.END
