from enum import Enum

from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

from app.telefix.common.helpers import num_tokens_from_string


class CheckRemainingTokensCallbackEventType(Enum):
    CHECK = 0


class CheckRemainingTokensCallback:
    def __init__(self, config):
        self._config = config
        self._event_callbacks = {
            CheckRemainingTokensCallbackEventType.CHECK: self._check_remaining_tokens_callback,
        }

    @staticmethod
    def get_event(_update: Update, _context: ContextTypes.DEFAULT_TYPE):
        return CheckRemainingTokensCallbackEventType.CHECK

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

        event = self.get_event(update, context)
        await self._event_callbacks[event](update, context)

    async def _check_remaining_tokens_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Sends a message to the user with the amount of tokens he has left in his current conversation"""
        conversation_history = (
            context.user_data["GPT_premium_conversation"]
            if context.user_data["GPT_premium"]
            else context.user_data["GPT_conversation"]
        )
        conversation_tokens = sum(
            num_tokens_from_string(message["content"])
            for message in conversation_history
        )
        remaining_tokens = (
            self._config.model.limit_conversation_tokens - conversation_tokens
        )

        await update.message.reply_text(
            f"You currently have {remaining_tokens} tokens left"
        )
