from telegram.ext import CommandHandler

from yaserviceru.common.types import HandlerGroupType
from .start import start


class StartHandler:
    commands = ["start"]

    def __init__(self):
        self.commands = StartHandler.commands
        self.start_handler = CommandHandler(self.commands[0], start)

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [self.start_handler],
        }
