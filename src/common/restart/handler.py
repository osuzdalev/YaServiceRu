from telegram.ext import CommandHandler

from .restart import restart
from src.common.types import HandlerGroupType


class RestartHandler:
    tg = True
    commands = ["restart"]

    def __init__(self):
        self.commands = RestartHandler.commands
        self.restart_handler = CommandHandler(self.commands[0], restart)

    def get_handlers(self):
        return {HandlerGroupType.MESSAGE_COLLECTION.value: [self.restart_handler]}
