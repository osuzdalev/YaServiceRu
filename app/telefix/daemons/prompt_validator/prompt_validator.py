from typing import List, Tuple, Dict

from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from app.telefix.common.helpers import num_tokens_from_string


async def validate_prompt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    chatgpt_model_config,
    vector_db_client,
) -> None:
    """
    Asynchronously validates the user's prompt based on specified criteria.

    This function performs a three-step validation on the user's prompt to ensure that it meets
    the requirements for processing. It first checks if the ChatGPT chat is active. If it is,
    it then verifies that the prompt does not exceed the maximum allowed token limit. Finally,
    it ensures that the prompt is semantically aligned with the application's purpose.

    If the prompt fails any of these checks, a message is sent back to the user informing them
    of the issue, and an ApplicationHandlerStop exception is raised to halt further processing.

    Parameters:
    - chatgpt_model_config : Configuration object containing the settings and limitations
                             of the ChatGPT model.
    - vector_db_client : The client interface for interacting with the vector database,
                         used in semantic checks.

    Returns:
    - None : This function does not return any value but raises an exception to halt
             the processing if the validation fails.

    Raises:
    - ApplicationHandlerStop : Raised to stop the application handler if the validation fails.

    Usage Example:
    await validate_prompt(update, context, chatgpt_model_config, vector_db_client)
    """
    user = update.effective_user
    logger.info(f"({user.id}, {user.name}, {user.first_name})")

    # Todo UI/UX design needs to confirm this check
    if not context.user_data.get("GPT_active", False):
        await update.message.reply_text(
            "Похоже, вы не начали чат. Для этого используйте команду /chat"
        )
        raise ApplicationHandlerStop

    prompt = update.effective_message.text
    prompt_size_check, prompt_tokens = check_prompt_tokens(prompt, chatgpt_model_config)
    if not prompt_size_check:
        await update.message.reply_text(
            f"Текст запроса слишком длинный: {prompt_tokens} токенов (максимум {chatgpt_model_config.max_prompt_tokens})"
        )
        logger.info(f"({user.id}, {user.name}, {user.first_name}) - prompt too long")
        raise ApplicationHandlerStop

    if not check_prompt_semantic(prompt, vector_db_client):
        await update.message.reply_text(
            "Извините, но ваш вопрос выходит за рамки моей компетенции.\n"
            "Пожалуйста, задайте вопрос, связанный с ПО компьютеров, смартфонов, планшетов "
            "и подобных устройств."
        )
        raise ApplicationHandlerStop

    logger.info("Prompt cleared and passed to other handlers")


# Todo Should this be used in here or the ChatGPT module?
def check_conversation_tokens(
    prompt: str, conversation: List[Dict], chatgpt_model_config
) -> Tuple[bool, int]:
    """
    Checks if the conversation size, including the provided prompt, is within the token limit.
    Accounts for the minimum response token size that needs to be left after processing the user's message.
    """
    logger.info(" ")

    # Calculate tokens
    conversation_tokens = sum(
        num_tokens_from_string(message["content"], chatgpt_model_config.name)
        for message in conversation
    ) + num_tokens_from_string(prompt, chatgpt_model_config.name)
    remaining_tokens = (
        chatgpt_model_config.limit_conversation_tokens - conversation_tokens
    )

    if conversation_tokens < chatgpt_model_config.limit_conversation_tokens:
        return True, remaining_tokens
    else:
        return False, conversation_tokens


def check_prompt_tokens(prompt: str, chatgpt_model_config) -> Tuple[bool, int]:
    """
    Check if the message sent size is within bounds.
    Returns a tuple with a boolean and the amount of remaining tokens
    """
    logger.info(" ")

    # Calculate tokens
    prompt_tokens = num_tokens_from_string(prompt, chatgpt_model_config.name)
    remaining_tokens = chatgpt_model_config.max_prompt_tokens - prompt_tokens
    logger.info(f"PROMPT TOKEN SIZE: {prompt_tokens}")

    if prompt_tokens < chatgpt_model_config.max_prompt_tokens:
        return True, remaining_tokens
    else:
        return False, prompt_tokens


def check_prompt_semantic(prompt: str, vector_db_client) -> bool:
    """
    Check the semantic validity of the given prompt using vector similarity.

    This function evaluates if the provided prompt is semantically valid by encoding the prompt
    into a vector and comparing it to predefined English and Russian filters using the vector
    database client. The function calculates the average certainty of the prompt being
    semantically close to the filters and compares it against a predefined semantic threshold.

    Parameters:
    - prompt : str : The user's prompt or message text to be evaluated for semantic validity.
    - vector_db_client : Object : The client interface for the vector database used for
                                  encoding and comparing the prompt.

    Returns:
    - bool : Returns True if the average certainty of the prompt being semantically valid
             is greater or equal to the semantic threshold; otherwise, returns False.
    """
    logger.info(" ")

    # Vector Query
    logger.info(f"ENCODING PROMPT: {prompt}")
    embeddings = vector_db_client.embedding_model.encode(prompt)

    # Retrieve English filters
    logger.info("COMPARING TO ENGLISH FILTERS")
    english_vector_query_result = vector_db_client.vector_query(
        "EnglishFilters", embeddings
    )

    # Retrieve Russian filters
    logger.info("COMPARING TO RUSSIAN FILTERS")
    russian_vector_query_result = vector_db_client.vector_query(
        "RussianFilters", embeddings
    )

    # Combine both query results
    combined_query_results = english_vector_query_result + russian_vector_query_result

    if not combined_query_results:
        return False

    # Calculate average certainty
    total_certainty = sum(
        article["_additional"]["certainty"]
        for article in combined_query_results
    )
    average_certainty = total_certainty / len(combined_query_results)

    return average_certainty >= vector_db_client.semantic_threshold
