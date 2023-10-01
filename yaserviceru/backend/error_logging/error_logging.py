import html
import json
import logging
import smtplib as smtp
import traceback

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

logger_error = logging.getLogger(__name__)


async def send_email(
    _: Update, context: ContextTypes.DEFAULT_TYPE, content: str
) -> None:
    """Sends an email with the logs to the developer"""
    yaserviceru_email = context.bot_data["config"]["yaserviceru"]["app"]["email"][
        "call_center"
    ]
    password = context.bot_data["config"]["yaserviceru"]["secret"]["password_smtp"]

    message = "\r\n".join(
        [
            f"From: {yaserviceru_email}",
            f"To: {yaserviceru_email}",
            "Subject: YaServiceRu ERROR",
            "",
            content,
        ]
    )

    server = smtp.SMTP(
        context.bot_data["config"]["yaserviceru"]["app"]["email"]["smtp"]["url"],
        context.bot_data["config"]["yaserviceru"]["app"]["email"]["smtp"]["port"],
    )
    server.set_debuglevel(1)
    server.starttls()
    server.login(yaserviceru_email, password)
    server.sendmail(yaserviceru_email, yaserviceru_email, message.encode("utf-8"))
    server.quit()


async def error_notification(
    update: object, context: ContextTypes.DEFAULT_TYPE
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
        chat_id=context.bot_data["config"]["yaserviceru"]["app"]["tg_id"]["dev"],
        text=tg_message,
        parse_mode=ParseMode.HTML,
    )
    # and to the email
    await send_email(update, context, mail_message)
