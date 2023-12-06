from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

from . import (
    StartCallback,
    StopCallback,
    RequestCallback,
    PaymentLaunchCallback,
    CheckRemainingTokensCallback,
)
from ..config import ChatGPTConfig
from ..types import ChatGptCallbackType


class ChatGptCallbackHandler:
    def __init__(self, config: ChatGPTConfig = None):
        self._config = config

        self._callbacks = {
            ChatGptCallbackType.START: StartCallback(self._config),
            ChatGptCallbackType.STOP: StopCallback(),
            ChatGptCallbackType.REQUEST: RequestCallback(self._config),
            ChatGptCallbackType.PAYMENT_LAUNCH: PaymentLaunchCallback(self._config),
            ChatGptCallbackType.CHECK_REMAINING_TOKENS: CheckRemainingTokensCallback(
                self._config
            ),
        }

    def get_callback(self, callback_type: ChatGptCallbackType):
        return self._callbacks[callback_type]

    async def precheckout_callback(
        self, update: Update, _: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Answers the PreCheckoutQuery"""
        query = update.pre_checkout_query
        # check the payload, is it from this core and about this service?
        if query.invoice_payload == self._config.checkout_variables.extended_payload:
            logger.info(
                f"EXTENDED_PAYLOAD: {self._config.checkout_variables.extended_payload}"
            )
            logger.info(" ")
            await query.answer(ok=True)

    async def successful_payment_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the successful payment. Set the user to Premium category and update conversation database"""
        user = update.message.from_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

        # update.message.successful_payment.invoice_payload == ?

        context.user_data["GPT_premium"] = True
        context.user_data["GPT_premium_conversation"] = context.user_data["GPT_history"]
        context.user_data["GPT_history"] = self._config.model.conversation_init

        await update.message.reply_text("Thank you for your payment!")
