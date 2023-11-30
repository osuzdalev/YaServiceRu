from telegram.ext import CommandHandler

from ...common.types import TgHandlerPriority, TgModuleType
from .start import start


class StartHandler:
    TYPE = TgModuleType.START
    COMMANDS = ["start"]

    def __init__(self):
        self.start_handler = CommandHandler(self.COMMANDS[0], start)

    def get_handlers(self):
        return {
            TgHandlerPriority.CLIENT_BASIC: [self.start_handler],
        }
