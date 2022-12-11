from configparser import ConfigParser
import html
import json
import logging
import smtplib as smtp
import traceback

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

logger_error = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


def send_email(content: str) -> None:
    """Sends an email with the logs to the developer"""
    email = constants.get("EMAIL", "YANDEX")
    password = constants.get("PASSWORD", "YANDEX_APP")

    message = "\r\n".join([
        f"From: {email}",
        "To: {}".format(constants.get("EMAIL", "YANDEX")),
        "Subject: YaServiceRu ERROR",
        "",
        content
    ])

    server = smtp.SMTP('smtp.yandex.ru', 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message.encode('utf-8'))
    server.quit()


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger_error.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096-character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    tg_message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    mail_message = (
        "An exception was raised while handling an update\n"
        f"update = {json.dumps(update_str, indent=2, ensure_ascii=False)}"
        "\n\n"
        f"context.chat_data = {str(context.chat_data)}\n\n"
        f"context.user_data = {str(context.user_data)}\n\n"
        f"{tb_string}"
    )

    # Finally, send the message
    await context.bot.send_message(chat_id=constants.get("ID", "MAIN"), text=tg_message, parse_mode=ParseMode.HTML)
    send_email(mail_message)
