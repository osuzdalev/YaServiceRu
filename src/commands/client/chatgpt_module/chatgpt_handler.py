from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    PreCheckoutQueryHandler,
)

from src.common.global_fallback.global_fallback import ignored_texts_re
from src.commands.client.chatgpt_module.chatgpt_config import ChatGPTConfig
from src.commands.client.chatgpt_module.chatgpt import (
    gpt_start,
    gpt_stop,
    gpt_request,
    gpt_payment_yes,
    gpt_payment_no,
    gpt_precheckout_callback,
    gpt_successful_payment_callback,
    gpt_get_remaining_tokens
)
from src.common.types import HandlerGroupType

CHATGPT_CONFIG = ChatGPTConfig()


class ChatGptHandler:
    def __init__(self):
        self.gpt_handler_command = CommandHandler("chat", gpt_start)
        self.gpt_handler_message = MessageHandler(
            filters.Regex(r"^🤖Чат с подержкой$"), gpt_start
        )

        self.gpt_request_handler = MessageHandler(
            filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND),
            gpt_request,
        )

        self.gpt_payment_yes_handler = MessageHandler(
            filters.Regex(r"^{}$".format(CHATGPT_CONFIG.confirm_payment)), gpt_payment_yes
        )
        self.gpt_precheckout_handler = PreCheckoutQueryHandler(gpt_precheckout_callback)
        # TODO add condition specific to chatgpt payment
        self.gpt_successful_payment_handler = MessageHandler(
            filters.SUCCESSFUL_PAYMENT, gpt_successful_payment_callback
        )
        self.gpt_payment_no_handler = MessageHandler(
            filters.Regex(r"^{}$".format(CHATGPT_CONFIG.decline_payment)), gpt_payment_no
        )

        self.gpt_stop_handler_command = CommandHandler("chat_stop", gpt_stop)
        self.gpt_stop_handler_message = MessageHandler(
            filters.Regex(r"^❌Отменить$"), gpt_stop
        )

        self.gpt_get_remaining_tokens_handler = CommandHandler(
            "token", gpt_get_remaining_tokens
        )

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [self.gpt_handler_command,
                                                  self.gpt_handler_message,
                                                  self.gpt_request_handler,
                                                  self.gpt_stop_handler_command,
                                                  self.gpt_stop_handler_message,
                                                  self.gpt_get_remaining_tokens_handler],
            HandlerGroupType.CLIENT_PAY.value: [self.gpt_payment_yes_handler,
                                                self.gpt_precheckout_handler,
                                                self.gpt_successful_payment_handler,
                                                self.gpt_payment_no_handler],
        }
