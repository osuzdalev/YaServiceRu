from enum import Enum

from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes


class StopCallbackEventType(Enum):
    CHATGPT_ACTIVATED = 0


class StopCallback:
    def __init__(self):
        self._event_callbacks = {
            StopCallbackEventType.CHATGPT_ACTIVATED: self._chatgpt_activated_callback,
        }

    @staticmethod
    def get_event(_update: Update, _context: ContextTypes.DEFAULT_TYPE):
        return StopCallbackEventType.CHATGPT_ACTIVATED

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

        event = self.get_event(update, context)
        await self._event_callbacks[event](update, context)

    @staticmethod
    async def _chatgpt_activated_callback(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        context.user_data["GPT_active"] = False
        await update.message.reply_text(
            "YaService-GPT остановлен.\n"
            "Ваши сообщения больше не будут отправляться на YaService-GPT."
        )
