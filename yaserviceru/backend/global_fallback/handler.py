from telegram.ext import MessageHandler, filters

from yaserviceru.common.types import HandlerGroupType
from .unknown_command import unknown_command


class GlobalFallbackHandler:
    def __init__(self, commands=None, messages=None):
        self.commands = commands if commands else []
        self.messages = messages if messages else []
        self.ignore_commands_re = (
            r"^(" + "|".join("\\" + "/" + command for command in self.commands) + ")$"
        )
        self.ignore_messages_re = (
            r"^(" + "|".join(message for message in self.messages) + ")$"
        )

        self.global_fallback_handler = MessageHandler(
            filters.COMMAND & (~filters.Regex(self.ignore_commands_re)), unknown_command
        )

    def get_handlers(self):
        return {
            HandlerGroupType.GLOBAL_FALLBACK.value: [self.global_fallback_handler],
        }