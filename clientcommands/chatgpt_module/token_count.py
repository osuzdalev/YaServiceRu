import tiktoken


def num_tokens_from_string(string: str, model_name: str = "gpt-3.5-turbo") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    with open("/clientcommands/chatgpt_module/chatgpt_data/test.txt", "r") as file:
        test_str = file.read()
    tokens = num_tokens_from_string(test_str)
    print(tokens)
