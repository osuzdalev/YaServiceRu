from typing import List

from telegram.ext import MessageHandler, filters

from ...common.types import TgHandlerPriority, TgModuleType
from .unknown_command import unknown_command


class GlobalFallbackHandler:
    TYPE = TgModuleType.GLOBAL_FALLBACK

    def __init__(self, commands: List, messages: List):
        self.COMMANDS = commands or []
        self.MESSAGES = messages or []
        self.ignore_commands_re = (
            r"^(" + "|".join(rf"\/{command}" for command in self.COMMANDS) + ")$"
        )
        self.ignore_messages_re = r"^(" + "|".join(self.MESSAGES) + ")$"

        self.global_fallback_handler = MessageHandler(
            filters.COMMAND & (~filters.Regex(self.ignore_commands_re)), unknown_command
        )

    def get_handlers(self):
        return {
            TgHandlerPriority.GLOBAL_FALLBACK: [self.global_fallback_handler],
        }
