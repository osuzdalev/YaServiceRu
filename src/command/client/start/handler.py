from telegram.ext import (
    CommandHandler,
)

from src.command.client.start.start import start
from src.common.types import HandlerGroupType


class StartHandler:
    tg = True
    commands = ["start"]

    def __init__(self):
        self.commands = StartHandler.commands
        self.start_handler = CommandHandler(self.commands[0], start)

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [self.start_handler],
        }
