import tiktoken


def num_tokens_from_string(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    test_str = "You’re a senior developer. You’ve been doing this for 20 years. " \
               "English is your native language and the only one you will use." \
               "We are a company developing a bot on the Telegram messenger application with the Python Telegram Bot. " \
               "We need you to take a look at some of our code and help us with a task. " \
               "You will rewrite, debug, and optimize our existing code based on the task at hand." \
               "In your answers, you will only send the parts of the code that are altered or added, " \
               "along with concise comments and the line numbers. NEVER send the entire code back."
    tokens = num_tokens_from_string(test_str)
    print(tokens)
