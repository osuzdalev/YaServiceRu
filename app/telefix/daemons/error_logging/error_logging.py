import html
import json
import logging
import traceback

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from email.mime.text import MIMEText

logger_error = logging.getLogger(__name__)


async def send_email(
    _: Update, context: ContextTypes.DEFAULT_TYPE, mail_server, mail_message: str
) -> None:
    """Sends an email with the logs to the developer"""
    email = context.bot_data["config"]["telefix"]["contact"]["email"]["dev"]
    password = context.bot_data["config"]["telefix"]["secret"]["password_smtp"]

    msg = MIMEText(mail_message)
    msg["From"] = email
    msg["To"] = email
    msg["Subject"] = "YaServiceRu ERROR"

    mail_server.login(email, password)
    mail_server.send_message(msg)
    mail_server.quit()


async def error_notification(
    update: object, context: ContextTypes.DEFAULT_TYPE, mail_server
) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger_error.error(
        msg="Exception while handling an update:", exc_info=context.error
    )

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # Might need to add some logic to deal with messages longer than the 4096-character limit.
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

    # Finally, send the message via telegram
    await context.bot.send_message(
        chat_id=context.bot_data["config"]["telefix"]["contact"]["tg_id"]["dev"],
        text=tg_message,
        parse_mode=ParseMode.HTML,
    )
    # and to the email
    await send_email(update, context, mail_server, mail_message)
