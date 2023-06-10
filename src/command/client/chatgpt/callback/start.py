from enum import Enum

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode


class StartCallbackEventType(Enum):
    FIRST_TIME_USER = 0
    EXISTING_USER = 1
    MAXED_OUT_USER = 2


class StartCallback:
    def __init__(self, logger, config):
        self._logger = logger
        self._config = config
        self._event_callbacks = {
            StartCallbackEventType.FIRST_TIME_USER: self._first_time_user_cb,
            StartCallbackEventType.EXISTING_USER: self._existing_user_cb,
            StartCallbackEventType.MAXED_OUT_USER: self._maxed_out_user_cb,
        }

    def get_event(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if "GPT_level" not in context.user_data:
            return StartCallbackEventType.FIRST_TIME_USER
        if (
            context.user_data["GPT_level"] in (0, 1)
            and context.user_data["GPT_messages_sent"] < self._config.model.free_prompt_limit
        ):
            return StartCallbackEventType.EXISTING_USER
        if (
            context.user_data["GPT_level"] == 1
            and context.user_data["GPT_messages_sent"] >= self._config.model.free_prompt_limit
        ):
            return StartCallbackEventType.MAXED_OUT_USER
        raise RuntimeError("Unknown event type StartCallbackEventType")

    async def __call__(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self.__class__.__qualname__}"
        )

        event = self.get_event(update, context)
        await self._event_callbacks[event](update, context)

    async def _first_time_user_cb(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        context.user_data["GPT_active"] = True
        context.user_data["GPT_level"] = 0
        context.user_data["GPT_messages_sent"] = 0
        context.user_data["GPT_premium"] = False
        context.user_data["GPT_conversation"] = self._config.gpt_conversation_start
        context.user_data[
            "GPT_premium_conversation"
        ] = self._config.gpt_conversation_start

        await update.message.reply_text(
            "Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
            "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop".format(
                self._config.free_prompt_limit - context.user_data["GPT_messages_sent"]
            )
        )

    async def _existing_user_cb(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        context.user_data["GPT_active"] = True
        await update.message.reply_text(
            "Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
            "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop".format(
                self._config.model.free_prompt_limit - context.user_data["GPT_messages_sent"]
            )
        )

    async def _maxed_out_user_cb(
            self, update: Update, _: ContextTypes.DEFAULT_TYPE
    ):
        await update.message.reply_text(
            self._config.max_messages_string, parse_mode=ParseMode.MARKDOWN_V2
        )
