import os

from sentence_transformers import SentenceTransformer
import torch

from clientcommands.chatgpt_module.token_count import num_tokens_from_string
from clientcommands.chatgpt_module.Weaviate.weaviate_client import WeaviateClient

INSTRUCTIONS_PATH = "system_instructions.txt"
FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), INSTRUCTIONS_PATH)
with open(FULL_PATH, "r") as file:
    instructions = file.read()
GPT_CONVERSATION_START = [{"role": "system", "content": instructions}]

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.6
MAX_RESPONSE_TOKENS = 350
TOP_P = 0.9
FREQUENCY_PENALTY = 1.0
PRESENCE_PENALTY = 0.3

FREE_PROMPT_LIMIT = 100
EXTENDED_PAYLOAD = "GPT_extended_payload"
LABEL = "YaService-GPT extension"

MAX_CONVERSATION_TOKENS = 4096
# Amount of tokens in a conversation to at least get a minimum response
LIMIT_CONVERSATION_TOKENS = MAX_CONVERSATION_TOKENS - MAX_RESPONSE_TOKENS
INSTRUCTIONS_TOKENS = num_tokens_from_string(instructions)
MAX_SUM_RESPONSE_TOKENS = FREE_PROMPT_LIMIT * MAX_RESPONSE_TOKENS
# max size prompt to at least get one answer
MAX_PROMPT_TOKENS = MAX_CONVERSATION_TOKENS - INSTRUCTIONS_TOKENS - MAX_RESPONSE_TOKENS

CONFIRM_PAYMENT = "CONFIRM_CHATGPT_PAYMENT"
DECLINE_PAYMENT = "DECLINE_CHATGPT_PAYMENT"
MAX_MESSAGES_STRING = "Вы достигли лимита бесплатного взаимодействия с нашим LLM\. " \
                      "Если вы хотите продолжить получать помощь от нашего LLM, " \
                      "мы предлагаем опцию оплаты за использование, которая позволяет продлить разговор\. " \
                      "Пожалуйста, обратите внимание, что этот продленный разговор будет ограничен 4096 символами, " \
                      "обеспечивая фокусированное и эффективное взаимодействие\. " \
                      "\n\nЧтобы продолжить с опцией оплаты за использование, введите `{}`, " \
                      "а затем следуйте инструкциям для оплаты\. " \
                      "Если вы не хотите продолжать, введите `{}` и не стесняйтесь обращаться к нам в будущем, " \
                      "если вам потребуется помощь\.".format(CONFIRM_PAYMENT, DECLINE_PAYMENT)


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
EMBEDDING_MODEL = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
SEMANTIC_THRESHOLD = 0.75
QUERY_LIMIT = 10

# Initialize the WeaviateClient
weaviate_client = WeaviateClient()
