from dataclasses import dataclass

from src.app.data_reader import DataReader
from src.common.helpers import num_tokens_from_string


data_reader = DataReader()


@dataclass
class Model:
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
    instructions_tokens: int = num_tokens_from_string(data_reader.chatgpt.get_system_instructions(), name)
    max_sum_response_tokens: int = free_prompt_limit * max_response_tokens
    # max size prompt to at least get one answer
    max_prompt_tokens: int = (
        max_conversation_tokens - instructions_tokens - max_response_tokens
    )
    conversation_init = [
        {"role": "system", "content": data_reader.chatgpt.get_system_instructions()}
    ]


@dataclass
class Messages:
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
class CheckoutVariables:
    extended_payload: str = "GPT_extended_payload"
    extended_label: str = "YaService-GPT extension"


@dataclass
class ChatGPTConfig:
    model: Model = Model()
    messages: Messages = Messages()
    checkout_variables: CheckoutVariables = CheckoutVariables()
