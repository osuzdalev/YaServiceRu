import pathlib
import re
from loguru import logger
from typing import List

from telegram import InlineKeyboardMarkup, Update, LabeledPrice
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackQueryHandler


class Page:
    """
    Represents a single page within a Telegram bot's interactive website-like interface.

    This class encapsulates the properties and behaviors of a page, including its name, title,
    associated messages, keyboard layout, invoice handling, and navigation functionality.

    Attributes:
        name (str): Identifier of the page.
        title (str): Title of the page, displayed at the top.
        messages (dict): Optional additional messages to be sent when the page is displayed.
        keyboard (List[List]): Keyboard layout for the page's inline buttons.
        invoice (optional): Information for handling invoice-related actions.
        return_state (optional): State to return after handling the page.
        browser_history_name (optional): Key name for storing browsing history in context.
        handlers (List): List of Telegram's CallbackQueryHandlers for the page.

    Methods:
        handler_callback(update, context): Handles callbacks triggered by the page's buttons.
        invoice_handler_callback(update, context): Handles invoice-related callbacks.
    """

    def __init__(
        self,
        name: str,
        title: str,
        messages: dict,
        keyboard: List[List],
        invoice=None,
        return_state=None,
        browser_history_name=None,
        media_dir: pathlib = None,
    ):
        self.name = name
        self.title = title
        self.messages = messages
        self.keyboard = keyboard
        self.invoice = invoice
        self.return_state = return_state
        self.browser_history_name = browser_history_name
        self.media_dir = media_dir
        self.handlers = []

        self.handlers.append(
            CallbackQueryHandler(self.handler_callback, pattern=self.name)
        )
        if self.invoice:
            self.handlers.append(
                CallbackQueryHandler(
                    self.invoice_handler_callback,
                    pattern=self.invoice["callback_pattern"],
                )
            )

    async def handler_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        query = update.callback_query
        await query.answer()

        logger.debug(f"This is the handler callback for the page {self.name}")
        logger.debug(f"Listening to callback_data {update.callback_query.data}")
        logger.debug(f"Buttons are: {self.keyboard}")

        # Save the current page in browsing history
        browser_history = context.user_data[self.browser_history_name]
        browser_history.append(self.name)
        logger.debug(browser_history)

        # Save the context for request_module message to expert
        pattern = r"[_*]+"
        output_text = re.sub(pattern, "", self.title)
        context.user_data["Device_Context"].append(output_text)

        # Checking if there are annex messages to be sent also
        if self.messages:
            for key in self.messages:
                if self.messages[key][0] == "text":
                    message = await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=self.messages[key][1],
                        parse_mode=ParseMode.MARKDOWN_V2,
                    )
                    context.user_data["Annexe_Messages"].append(message)
                elif self.messages[key][0] == "picture":
                    # TODO Upgrade to use file_id, maybe be significantly faster
                    file_path = self.media_dir / self.messages[key][1]
                    with open(file_path, "rb") as photo:
                        message = await context.bot.send_photo(
                            chat_id=update.effective_chat.id, photo=photo
                        )
                    context.user_data["Annexe_Messages"].append(message)

        await query.edit_message_text(
            text=self.title,
            reply_markup=InlineKeyboardMarkup(self.keyboard),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        return self.return_state

    async def invoice_handler_callback(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Sends an invoice without shipping-payment."""
        query = update.callback_query
        user = query.from_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")
        await query.answer()

        logger.debug(
            f"This is the invoice_handler_callback for the page {self.page.name}"
        )
        logger.debug(f"My buttons are: {self.page.keyboard}")

        chat_id = update.effective_chat.id
        title = self.invoice["title"]
        description = self.invoice["description"]
        # select a payload just for you to recognize it's the donation from your bot
        payload = self.invoice["payload"]
        currency = self.invoice["currency"]
        price = self.invoice["price"]
        label = self.invoice["label"]
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
            chat_id,
            title,
            description,
            payload,
            context.bot_data["config"].core.secret.token_payment_provider,
            currency,
            prices,
        )
