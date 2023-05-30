import logging
from typing import List, Tuple, Dict

from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes

from resources.constants_loader import load_constants

from clientcommands.chatgpt_module.chatgpt_data.config import *
from clientcommands.chatgpt_module.token_count import num_tokens_from_string

logger_chatgpt = logging.getLogger(__name__)
constants = load_constants()


def check_conversation_tokens(
    prompt: str, conversation: List[Dict]
) -> Tuple[bool, int]:
    """Checks if the conversation size, including the provided prompt, is within the token limit.
    Accounts for the minimum response token size that needs to be left after processing the user's message.
    """

    # Calculate tokens
    conversation_tokens = sum(
        num_tokens_from_string(message["content"]) for message in conversation
    ) + num_tokens_from_string(prompt)
    remaining_tokens = LIMIT_CONVERSATION_TOKENS - conversation_tokens

    return (
        (True, remaining_tokens)
        if conversation_tokens < LIMIT_CONVERSATION_TOKENS
        else (False, conversation_tokens)
    )


def check_prompt_tokens(prompt: str) -> Tuple[bool, int]:
    """Check if the sent message size is within bounds.
    Returns a tuple with a boolean and the amount of remaining tokens"""
    # Calculate tokens
    prompt_tokens = num_tokens_from_string(prompt)
    remaining_tokens = MAX_PROMPT_TOKENS - prompt_tokens
    logger_chatgpt.info("prompt_size_check: {}".format(prompt_tokens))

    return (
        (True, remaining_tokens)
        if prompt_tokens < MAX_PROMPT_TOKENS
        else (False, prompt_tokens)
    )


def check_prompt_semantic(prompt: str) -> bool:
    # Vector Query
    logger_chatgpt.info("embedding: {}".format(prompt))
    embeddings = EMBEDDING_MODEL.encode(prompt)

    # Retrieve English filters
    logger_chatgpt.info("retrieving English filters")
    english_vector_query_result = weaviate_client.vector_query(
        "EnglishFilters", embeddings
    )

    # Retrieve Russian filters
    logger_chatgpt.info("retrieving Russian filters")
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

    if average_certainty >= SEMANTIC_THRESHOLD:
        return True
    else:
        return False


async def validate_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Checks if the prompt is valid in three steps:
    1. Check if the user is in a conversation
    2. Check if the prompt is within the token limit
    3. Check if the prompt is semantically close enough to the bot's purpose"""
    user = update.message.from_user

    if not context.user_data.get("GPT_active", False):
        await update.message.reply_text(
            "Похоже, вы не начали чат. Для этого используйте команду '/chat'"
        )
        return False

    prompt = update.effective_message.text
    prompt_size_check, prompt_tokens = check_prompt_tokens(prompt)
    if not prompt_size_check:
        await update.message.reply_text(
            "Текст запроса слишком длинный: {} токенов (максимум {})".format(
                prompt_tokens, MAX_PROMPT_TOKENS
            )
        )
        logger_chatgpt.info(
            "({}, {}, {}) - prompt too long".format(user.id, user.name, user.first_name)
        )
        return False

    if not check_prompt_semantic(prompt):
        await update.message.reply_text(
            "Извините, но ваш вопрос выходит за рамки моей компетенции.\n"
            "Пожалуйста, задайте вопрос, связанный с ПО компьютеров, смартфонов, планшетов "
            "и подобных устройств."
        )
        return False

    return True
