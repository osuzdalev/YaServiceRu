from enum import Enum

from telegram import Update
from telegram.ext import ContextTypes


class StopCallbackEventType(Enum):
    CHATGPT_ACTIVATED = 0


class StopCallback:
    def __init__(self, logger):
        self._logger = logger
        self._event_callbacks = {
            StopCallbackEventType.CHATGPT_ACTIVATED: self._chatgpt_activated_callback,
        }

    @staticmethod
    def get_event(_: Update, context: ContextTypes.DEFAULT_TYPE):
        if context.user_data.get("GPT_active", False):
            return StopCallbackEventType.CHATGPT_ACTIVATED
        raise RuntimeError("Unknown event type StopCallbackEventType")

    async def __call__(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self.__class__.__qualname__}"
        )

        event = self.get_event(update, context)
        await self._event_callbacks[event](update, context)

    @staticmethod
    async def _chatgpt_activated_callback( update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["GPT_active"] = False
        await update.message.reply_text(
            "YaService-GPT остановлен.\n"
            "Ваши сообщения больше не будут отправляться на YaService-GPT."
        )
