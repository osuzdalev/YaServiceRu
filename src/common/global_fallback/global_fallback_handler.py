from telegram.ext import (
    MessageHandler,
    filters,
)

from src.common.global_fallback.global_fallback import (
    unknown_command,
    ignored_commands_re,
)

from src.common.types import HandlerGroupType


class GlobalFallbackHandler:
    def __init__(self):
        self.global_fallback_handler = MessageHandler(
            filters.COMMAND & (~filters.Regex(ignored_commands_re)), unknown_command
        )

        self.global_fallback_handler_group = HandlerGroupType.GLOBAL_FALLBACK.value

    def get_handler(self):
        return self.global_fallback_handler

    def get_handler_group(self):
        return self.global_fallback_handler_group
