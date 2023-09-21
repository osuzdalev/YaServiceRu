import inspect
import logging
from typing import List, Tuple, Dict

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from src.common.helpers import num_tokens_from_string

logger_prompt_validator = logging.getLogger(__name__)


async def validate_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if the prompt is valid in three steps:
    1. Check if the ChatGPT canal is open
    2. Check if the prompt is within the token limit
    3. Check if the prompt is semantically close enough to the app's purpose"""
    user = update.effective_user
    logger_prompt_validator.info(
        f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
    )

    if not context.user_data.get("GPT_active", False):
        await update.message.reply_text(
            "Похоже, вы не начали чат. Для этого используйте команду /chat"
        )
        raise ApplicationHandlerStop

    prompt = update.effective_message.text
    prompt_size_check, prompt_tokens = check_prompt_tokens(prompt)
    if not prompt_size_check:
        await update.message.reply_text(
            "Текст запроса слишком длинный: {} токенов (максимум {})".format(
                prompt_tokens, chatgpt_config.model.max_prompt_tokens
            )
        )
        logger_prompt_validator.info(
            f"({user.id}, {user.name}, {user.first_name}) - prompt too long"
        )
        raise ApplicationHandlerStop

    if not check_prompt_semantic(prompt):
        await update.message.reply_text(
            "Извините, но ваш вопрос выходит за рамки моей компетенции.\n"
            "Пожалуйста, задайте вопрос, связанный с ПО компьютеров, смартфонов, планшетов "
            "и подобных устройств."
        )
        raise ApplicationHandlerStop

    return


def check_conversation_tokens(
    prompt: str, conversation: List[Dict]
) -> Tuple[bool, int]:
    """Checks if the conversation size, including the provided prompt, is within the token limit.
    Accounts for the minimum response token size that needs to be left after processing the user's message.
    """
    logger_prompt_validator.info(f"{inspect.currentframe().f_code.co_name}")

    # Calculate tokens
    conversation_tokens = sum(
        num_tokens_from_string(message["content"], chatgpt_config.model.name)
        for message in conversation
    ) + num_tokens_from_string(prompt, chatgpt_config.model.name)
    remaining_tokens = (
        chatgpt_config.model.limit_conversation_tokens - conversation_tokens
    )

    return (
        (True, remaining_tokens)
        if conversation_tokens < chatgpt_config.model.limit_conversation_tokens
        else (False, conversation_tokens)
    )


def check_prompt_tokens(prompt: str) -> Tuple[bool, int]:
    """Check if the message sent size is within bounds.
    Returns a tuple with a boolean and the amount of remaining tokens"""
    logger_prompt_validator.info(f"{inspect.currentframe().f_code.co_name}")

    # Calculate tokens
    prompt_tokens = num_tokens_from_string(prompt, chatgpt_config.model.name)
    remaining_tokens = chatgpt_config.model.max_prompt_tokens - prompt_tokens
    logger_prompt_validator.info(f"PROMPT TOKEN SIZE: {prompt_tokens}")

    return (
        (True, remaining_tokens)
        if prompt_tokens < chatgpt_config.model.max_prompt_tokens
        else (False, prompt_tokens)
    )


def check_prompt_semantic(prompt: str) -> bool:
    logger_prompt_validator.info(f"{inspect.currentframe().f_code.co_name}")

    # Vector Query
    logger_prompt_validator.info(f"ENCODING PROMPT: {prompt}")
    embeddings = weaviate_client.embedding_model.encode(prompt)

    # Retrieve English filters
    logger_prompt_validator.info("COMPARING TO ENGLISH FILTERS")
    english_vector_query_result = weaviate_client.vector_query(
        "EnglishFilters", embeddings
    )

    # Retrieve Russian filters
    logger_prompt_validator.info("COMPARING TO RUSSIAN FILTERS")
    russian_vector_query_result = weaviate_client.vector_query(
        "RussianFilters", embeddings
    )

    # Combine both query results
    combined_query_results = english_vector_query_result + russian_vector_query_result

    if not combined_query_results:
        return False

    # Calculate average certainty
    total_certainty = sum(
        [article["_additional"]["certainty"] for article in combined_query_results]
    )
    average_certainty = total_certainty / len(combined_query_results)

    if average_certainty >= weaviate_client.semantic_threshold:
        return True
    else:
        return False
