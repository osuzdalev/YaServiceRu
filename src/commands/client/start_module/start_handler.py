from telegram.ext import (
    CommandHandler,
)

from src.commands.client.start_module.start import start
from src.common.types import HandlerGroupType


class StartHandler:
    def __init__(self):
        self.start_handler = CommandHandler("start", start)

    def get_handlers(self):
        return {
            HandlerGroupType.CLIENT_BASIC.value: [self.start_handler],
        }
