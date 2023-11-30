from telegram.ext import CommandHandler

from .restart import restart
from ...common.types import TgHandlerPriority, TgModuleType


class RestartHandler:
    TYPE = TgModuleType.RESTART
    COMMANDS = ["restart"]

    def __init__(self):
        self.restart_handler = CommandHandler(self.COMMANDS[0], restart)

    def get_handlers(self):
        return {TgHandlerPriority.RESTART: [self.restart_handler]}
