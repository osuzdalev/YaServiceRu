from telegram.ext import (
    MessageHandler,
    filters,
)

from src.common.types import HandlerGroupType
from .prompt_validator import validate_prompt


class PromptValidatorHandler:
    def __init__(self, chatgpt_config, weaviate_client, ignore_messages_re):
        self.chatgpt_config = chatgpt_config
        self.weaviate_client = weaviate_client

        self.ignore_messages_re = ignore_messages_re
        self.validate_prompt_handler = MessageHandler(
            ~filters.COMMAND & ~filters.Regex(self.ignore_messages_re), validate_prompt
        )

    def get_handlers(self):
        return {
            HandlerGroupType.PROMPT_VALIDATION.value: [self.validate_prompt_handler]
        }
