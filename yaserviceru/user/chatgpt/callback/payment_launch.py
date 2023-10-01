import os
from enum import Enum

from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes


class PaymentLaunchCallbackEventType(Enum):
    PAYMENT_LAUNCH = 0


class PaymentLaunchCallback:
    def __init__(self, logger, config):
        self._logger = logger
        self._config = config
        self._event_callbacks = {
            PaymentLaunchCallbackEventType.PAYMENT_LAUNCH: self._payment_launch_callback,
        }

    @staticmethod
    def get_event(_update: Update, _context: ContextTypes.DEFAULT_TYPE):
        return PaymentLaunchCallbackEventType.PAYMENT_LAUNCH

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self.__class__.__qualname__}"
        )

        event = self.get_event(update, context)
        await self._event_callbacks[event](update, context)

    async def _payment_launch_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handles user's response to pay for more interactions."""
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self._payment_launch_callback.__qualname__}"
        )

        chat_id = update.message.chat_id
        title = "YaService-GPT Premium"
        description = "Увеличить длину разговора до 4096 токенов."
        # select a payload just for you to recognize its the donation from your app
        payload = self._config.checkout_variables.extended_payload
        currency = "RUB"
        price = 100
        # price * 100 to include 2 decimal points
        prices = [
            LabeledPrice(self._config.checkout_variables.extended_label, price * 100)
        ]

        await context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            os.getenv("TOKEN_PAYMENT_PROVIDER_YOOKASSA"),
            currency,
            prices,
        )
