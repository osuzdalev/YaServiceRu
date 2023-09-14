from enum import Enum
from typing import List, Dict
import re

import openai
from openai import InvalidRequestError

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.common.prompt_validator import (
    validate_prompt,
    check_conversation_tokens,
)


class RequestCallbackEventType(Enum):
    FIRST_TIME_USER = 0
    UNDER_MESSAGE_LIMIT_USER = 1
    ABOVE_MESSAGE_LIMIT_USER = 2
    PREMIUM_USER = 3


class RequestCallback:
    def __init__(self, logger, config, data_reader):
        self._logger = logger
        self._config = config
        self._data_reader = data_reader
        self._reply_request_inline_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Обратиться к специалисту", callback_data="REQUEST_COMMAND"
                    )
                ]
            ]
        )
        self._event_callbacks = {
            RequestCallbackEventType.FIRST_TIME_USER: self._first_time_user,
            RequestCallbackEventType.UNDER_MESSAGE_LIMIT_USER: self._under_message_limit_user,
            RequestCallbackEventType.ABOVE_MESSAGE_LIMIT_USER: self._above_message_limit_user,
            RequestCallbackEventType.PREMIUM_USER: self._premium_user,
        }

    def get_event(
        self,
        _update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        user_level,
        is_premium,
    ):
        # First time using the chat feature
        if user_level == 0:
            return RequestCallbackEventType.FIRST_TIME_USER
        # Previously used the chat feature but still within test limit and not premium yet
        elif (
            user_level == 1
            and context.user_data["GPT_messages_sent"]
            < self._config.model.free_prompt_limit
            and not is_premium
        ):
            return RequestCallbackEventType.UNDER_MESSAGE_LIMIT_USER
        # Check if user sent 5 messages but did not upgrade to premium
        elif (
            user_level == 1
            and context.user_data["GPT_messages_sent"]
            >= self._config.model.free_prompt_limit
            and not is_premium
        ):
            return RequestCallbackEventType.ABOVE_MESSAGE_LIMIT_USER
        # Check if user paid for chatgpt service
        else:
            return RequestCallbackEventType.PREMIUM_USER

    async def __call__(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self.__class__.__qualname__}"
        )

        # Checking if user prompt is a valid question
        is_valid_prompt = await validate_prompt(update, context)
        if not is_valid_prompt:
            return

        user_level = context.user_data["GPT_level"]
        prompt = update.effective_message.text
        conversation = (
            context.user_data["GPT_premium_conversation"]
            if context.user_data["GPT_premium"]
            else context.user_data["GPT_conversation"]
        )
        is_premium = context.user_data["GPT_premium"]

        # Send a gif to let the user know the prompt is being handled
        loading_gif = await update.message.reply_video(
            self._data_reader.chatgpt.get_loading_gif()
        )

        event = self.get_event(update, context, user_level, is_premium)
        await self._event_callbacks[event](
            update, context, prompt, conversation, loading_gif
        )

    async def _first_time_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        prompt,
        conversation,
        loading_gif,
    ) -> None:
        context.user_data["GPT_level"] = 1
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = self._generate_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {self._config.model.free_prompt_limit - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=self._reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens,
                    self._config.model.limit_conversation_tokens,
                )
            )

    async def _under_message_limit_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        prompt,
        conversation,
        loading_gif,
    ) -> None:
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = self._generate_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {self._config.model.free_prompt_limit - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=self._reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens,
                    self._config.model.limit_conversation_tokens,
                )
            )

    async def _above_message_limit_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        prompt,
        conversation,
        loading_gif,
    ) -> None:
        await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
        # Propose CHATGPT extension by payment at end of 5 free messages
        await update.message.reply_text(
            self._config.messages.max_messages, parse_mode=ParseMode.MARKDOWN_V2
        )

    async def _premium_user(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        prompt,
        conversation,
        loading_gif,
    ) -> None:
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            # get the response
            response = self._generate_response(prompt, conversation)
            # Update the response message to include the remaining tokens
            response += f"\n\nОсталось {conversation_tokens} токенов"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=self._reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens,
                    self._config.model.limit_conversation_tokens,
                )
            )

    def _generate_response(self, user_message: str, conversation: List[Dict]) -> str:
        """
        Generates a response from the ChatGPT model given the user's message and the conversation history.

        Args:
            user_message (str): The message sent by the user to the chatbot.
            conversation (List[Dict]): A list of dictionary objects representing the conversation history, with each
                dictionary containing "role" (the speaker) and "content" (the message content).

        Returns:
            str: The response generated by the ChatGPT model.
        """
        self._logger.info(f"{self._generate_response.__qualname__}")

        conversation.append({"role": "user", "content": user_message})
        try:
            completion = openai.ChatCompletion.create(
                model=self._config.model.name,
                messages=conversation,
                temperature=self._config.model.temperature,
                max_tokens=self._config.model.max_response_tokens,
                top_p=self._config.model.top_p,
                frequency_penalty=self._config.model.frequency_penalty,
                presence_penalty=self._config.model.presence_penalty,
            )
        except InvalidRequestError as e:
            self._logger.error(f"InvalidRequestError: {e}")
            # Appending the context.user_data["conversation"]
            conversation[-1]["content"] = "[TOO_LONG]"

            response = "An error occurred while processing your request. Please try again with shorter text."
            conversation.append({"role": "assistant", "content": response})
            return response

        # Appending the context.user_data["conversation"]
        conversation.append(
            {"role": "assistant", "content": completion.choices[0].message["content"]}
        )
        response = re.sub(r"^\n{2}", "", completion.choices[0].message["content"])
        return response
