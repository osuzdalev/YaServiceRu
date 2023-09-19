from telegram.ext import (
    CommandHandler,
)

from src.command.client.start.start import start
from src.common.types import HandlerGroupType


class StartHandler:
    command = ["start"]

    def __init__(self, commands=None, messages=None):
        self.commands = commands if commands else []
        self.messages = messages if messages else []

        self.start_handler = CommandHandler(self.commands[0], start)

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [self.start_handler],
        }
