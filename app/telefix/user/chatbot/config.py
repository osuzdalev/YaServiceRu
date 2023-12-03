import pathlib
from dataclasses import dataclass, field
from typing import List

from ...core.data_reader import ChatGPTDataReader
from ...common.helpers import num_tokens_from_string


@dataclass
class ChatGPTModelConfig:
    deployment: str
    path: pathlib
    # FIXME passing the deployment argument deep into the code
    # reformat the DataReader class
    __DATA_READER: ChatGPTDataReader = field(init=False)
    instructions_tokens: int = field(init=False)
    # max size prompt to at least get one answer
    max_prompt_tokens: int = field(init=False)
    conversation_init: List[dict] = field(init=False)

    name: str = "gpt-3.5-turbo"
    temperature: float = 0.6
    max_response_tokens: int = 350
    top_p: float = 0.9
    frequency_penalty: float = 1.0
    presence_penalty: float = 0.3
    free_prompt_limit: int = 100
    max_conversation_tokens: int = 4096
    # Amount of tokens in a conversation to at least get a minimum response
    limit_conversation_tokens: int = max_conversation_tokens - max_response_tokens
    max_sum_response_tokens: int = free_prompt_limit * max_response_tokens

    def __post_init__(self):
        self.__DATA_READER = ChatGPTDataReader(self.deployment, self.path)
        self.instructions_tokens = num_tokens_from_string(
            self.__DATA_READER.get_system_instructions(), self.name
        )
        self.max_prompt_tokens = (
            self.max_conversation_tokens
            - self.instructions_tokens
            - self.max_response_tokens
        )
        self.conversation_init = [
            {"role": "system", "content": self.__DATA_READER.get_system_instructions()}
        ]


@dataclass
class ChatGPTMessagesConfig:
    confirm_payment: str = "CONFIRM_CHATGPT_PAYMENT"
    max_messages: str = f"""Вы достигли лимита бесплатного взаимодействия с нашим LLM.
    Если вы хотите продолжить получать помощь от нашего LLM,
    мы предлагаем опцию оплаты за использование, которая позволяет продлить разговор.
    Пожалуйста, обратите внимание, что этот продленный разговор будет ограничен 4096 символами,
    обеспечивая фокусированное и эффективное взаимодействие.
    
    Чтобы продолжить с опцией оплаты за использование, введите `{confirm_payment}`,
    а затем следуйте инструкциям для оплаты.
    Если вы не хотите продолжать не стесняйтесь обращаться к нам в будущем,
    если вам потребуется помощь."""


@dataclass
class ChatGPTCheckoutVariables:
    extended_payload: str = "GPT_extended_payload"
    extended_label: str = "YaService-GPT extension"


@dataclass
class ChatGPTConfig:
    deployment: str
    path: pathlib
    model: ChatGPTModelConfig = field(init=False)
    messages: ChatGPTMessagesConfig = ChatGPTMessagesConfig()
    checkout_variables: ChatGPTCheckoutVariables = ChatGPTCheckoutVariables()

    def __post_init__(self):
        self.model = ChatGPTModelConfig(deployment=self.deployment, path=self.path)
