import logging

from telegram import Update, PhotoSize
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode

from background import telegram_database_utils as tldb

logger_start = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stuff"""
    logger_start.info("start()")

    context.user_data['in_conversation'] = ''
    context.user_data["Device_Context"] = None

    # file_id = "AgACAgIAAxkBAAEaZ8Zjg_V9gCfMtNcDSjgJkDskCLjIpQAC28gxG-wcIEjay-bnmleibAEAAwIAA3MAAysE"
    # file_unique_id = "AQAD28gxG-wcIEh4"
    # test_size = PhotoSize(file_id, file_unique_id, 10, 10)
    # path = "/Users/osuz/Downloads/photo_2022-11-18 23.52.33.jpeg"
    # await update.message.reply_photo(path, caption="Some Caption")
    await update.message.reply_text("Welcome!\n"
                                    "/wiki - find an easy fix\n"
                                    "/request - contact customer service\n"
                                    "/pay - send a payment")
    # await update.message.reply_text("*text*\n"
    #                                 "_text_\n"
    #                                 "__text__\n"
    #                                 "~text~\n"
    #                                 "||__text__||\n"
    #                                 "*_~||italic bold strikethrough spoiler||~"
    #                                 "__underline italic bold__ _* text \n"
    #                                 "[text](http://www.example.com/)\n"
    #                                 "[text](tg://user?id=5278871996)\n"
    #                                 "`inline fixed-width code`\n"
    #                                 "```"
    #                                 "del pre-formated fixed width code block"
    #                                 "```\n",
    #                                 parse_mode=ParseMode.MARKDOWN_V2)

start_handler = CommandHandler("start", start)
