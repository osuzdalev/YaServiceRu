from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
)

from yaserviceru.user.chatgpt.config import ChatGPTConfig
from yaserviceru.user.chatgpt.callback.handler import ChatGptCallbackHandler
from yaserviceru.common.types import HandlerGroupType

from .types import ChatGptCallbackType


class ChatGptHandler:
    def __init__(self, ignored_texts_re):
        config = ChatGPTConfig()
        callback_handler = ChatGptCallbackHandler(config)

        callback_start = callback_handler.get_callback(ChatGptCallbackType.START)
        self.handler_command = CommandHandler("chat", callback_start)
        self.handler_message = MessageHandler(
            filters.Regex(r"^🤖Чат с подержкой$"), callback_start
        )

        callback_request = callback_handler.get_callback(ChatGptCallbackType.REQUEST)
        self.request_handler = MessageHandler(
            filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND),
            callback_request,
        )

        callback_payment_launch = callback_handler.get_callback(
            ChatGptCallbackType.PAYMENT_LAUNCH
        )
        self.payment_yes_handler = MessageHandler(
            filters.Regex(r"^{}$".format(config.messages.confirm_payment)),
            callback_payment_launch,
        )
        self.precheckout_handler = PreCheckoutQueryHandler(
            callback_handler.precheckout_callback
        )
        # TODO add condition specific to chatgpt payment
        self.successful_payment_handler = MessageHandler(
            filters.SUCCESSFUL_PAYMENT, callback_handler.successful_payment_callback
        )

        callback_stop = callback_handler.get_callback(ChatGptCallbackType.STOP)
        self.stop_handler_command = CommandHandler("chat_stop", callback_stop)
        self.stop_handler_message = MessageHandler(
            filters.Regex(r"^❌Отменить$"), callback_stop
        )

        callback_check_remaining_tokens = callback_handler.get_callback(
            ChatGptCallbackType.CHECK_REMAINING_TOKENS
        )
        self.get_remaining_tokens_handler = CommandHandler(
            "tokens", callback_check_remaining_tokens
        )

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [
                self.handler_command,
                self.handler_message,
                self.request_handler,
                self.stop_handler_command,
                self.stop_handler_message,
                self.get_remaining_tokens_handler,
            ],
            HandlerGroupType.CLIENT_PAY.value: [
                self.payment_yes_handler,
                self.precheckout_handler,
                self.successful_payment_handler,
            ],
        }