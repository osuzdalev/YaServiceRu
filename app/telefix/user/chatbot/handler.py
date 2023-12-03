from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
)

from .config import ChatGPTConfig
from .callback.handler import ChatGptCallbackHandler
from ...common.types import TgHandlerPriority, TgModuleType

from .types import ChatGptCallbackType


class ChatGptHandler:
    TYPE = TgModuleType.CHATBOT
    COMMANDS = ["chat", "chat_stop"]
    _MESSAGES = ["🤖Чат с подержкой", "❌Отменить"]

    def __init__(self, deployment: str, media: str, ignored_texts_re):
        config = ChatGPTConfig(deployment, media)
        callback_handler = ChatGptCallbackHandler(config)

        callback_start = callback_handler.get_callback(ChatGptCallbackType.START)
        self.handler_command = CommandHandler(self.COMMANDS[0], callback_start)
        self.handler_message = MessageHandler(
            filters.Regex(rf"^({self._MESSAGES[0]})$"), callback_start
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
        # TODO add condition specific to chatbot payment
        self.successful_payment_handler = MessageHandler(
            filters.SUCCESSFUL_PAYMENT, callback_handler.successful_payment_callback
        )

        callback_stop = callback_handler.get_callback(ChatGptCallbackType.STOP)
        self.stop_handler_command = CommandHandler(self.COMMANDS[1], callback_stop)
        self.stop_handler_message = MessageHandler(
            filters.Regex(rf"^({self._MESSAGES[1]})$"), callback_stop
        )

        callback_check_remaining_tokens = callback_handler.get_callback(
            ChatGptCallbackType.CHECK_REMAINING_TOKENS
        )
        self.get_remaining_tokens_handler = CommandHandler(
            "tokens", callback_check_remaining_tokens
        )

    def get_handlers(self):
        return {
            TgHandlerPriority.CLIENT_BASIC: [
                self.handler_command,
                self.handler_message,
                self.request_handler,
                self.stop_handler_command,
                self.stop_handler_message,
                self.get_remaining_tokens_handler,
            ],
            TgHandlerPriority.CLIENT_PAY: [
                self.payment_yes_handler,
                self.precheckout_handler,
                self.successful_payment_handler,
            ],
        }
