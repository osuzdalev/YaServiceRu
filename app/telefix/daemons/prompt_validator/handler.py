from functools import partial

from telegram.ext import MessageHandler, filters

from ...common.types import HandlerGroupType
from .prompt_validator import validate_prompt


class PromptValidatorHandler:
    def __init__(self, chatgpt_model_config, vector_db_client, ignore_messages_re):
        self.chatgpt_model_config = chatgpt_model_config
        self.vector_db_client = vector_db_client

        self.ignore_messages_re = ignore_messages_re
        self.validate_prompt_handler = MessageHandler(
            ~filters.COMMAND & ~filters.Regex(self.ignore_messages_re),
            partial(
                validate_prompt,
                chatgpt_model_config=self.chatgpt_model_config,
                vector_db_client=self.vector_db_client,
            ),
        )

    def get_handlers(self):
        return {
            HandlerGroupType.PROMPT_VALIDATION.value: [self.validate_prompt_handler]
        }
