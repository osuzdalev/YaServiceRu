from functools import partial

from telegram.ext import CommandHandler

from ...common.types import TgHandlerPriority, TgModuleType
from ...core.data_reader import StartReader
from .start import start


class StartHandler:
    TYPE = TgModuleType.START
    COMMANDS = ["start"]

    def __init__(self, deployment: str, data_path: str):
        self.start_reader: StartReader = StartReader(deployment, data_path)
        self.start_handler = CommandHandler(
            self.COMMANDS[0], partial(start, start_reader=self.start_reader)
        )

    def get_handlers(self):
        return {
            TgHandlerPriority.CLIENT_BASIC: [self.start_handler],
        }
