from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

from yaserviceru.user.request.request import (
    request,
    confirm_request,
    cancel_request,
)
from yaserviceru.common.types import HandlerGroupType


class RequestHandler:
    commands = ["request"]
    messages = ["🤓Специалист", "❌Отменить"]

    def __init__(self):
        self.request_command_handler = CommandHandler(self.commands[0], request)
        self.request_replykeyboard_handler = MessageHandler(
            filters.Regex(rf"^({self.messages[0]})$"), request
        )
        self.request_callback_handler = CallbackQueryHandler(
            request, pattern="REQUEST_COMMAND"
        )

        self.confirm_request_handler = CallbackQueryHandler(
            confirm_request, pattern="REQUEST_CALL_CONFIRM"
        )
        self.cancel_request_handler = CallbackQueryHandler(
            cancel_request, pattern="REQUEST_CALL_CANCEL"
        )
        self.cancel_request_handler_message = MessageHandler(
            filters.Regex(rf"^({self.messages[1]})$"), cancel_request
        )

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [
                self.request_command_handler,
                self.request_replykeyboard_handler,
                self.confirm_request_handler,
                self.cancel_request_handler,
                self.cancel_request_handler_message,
            ],
        }
