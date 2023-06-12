import tiktoken

# TODO: circular import error
# from src.command.client.chatgpt.config import ChatGPTConfig

# ChatGPTConfig = ChatGPTConfig()


def num_tokens_from_string(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
