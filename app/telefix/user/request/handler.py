from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters

from ...user.request.request import (
    request,
    confirm_request,
    cancel_request,
)
from ...common.types import TgHandlerPriority, TgModuleType


class RequestHandler:
    TYPE = TgModuleType.REQUEST
    COMMANDS = ["request"]
    _MESSAGES = ["🤓Специалист", "❌Отменить"]

    def __init__(self):
        self.request_command_handler = CommandHandler(self.COMMANDS[0], request)
        self.request_replykeyboard_handler = MessageHandler(
            filters.Regex(rf"^({self._MESSAGES[0]})$"), request
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
            filters.Regex(rf"^({self._MESSAGES[1]})$"), cancel_request
        )

    def get_handlers(self):
        return {
            TgHandlerPriority.CLIENT_BASIC: [
                self.request_command_handler,
                self.request_replykeyboard_handler,
                self.confirm_request_handler,
                self.cancel_request_handler,
                self.cancel_request_handler_message,
            ],
        }
