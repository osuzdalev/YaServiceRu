import logging
import os
import re
from typing import List, Dict

import openai
from openai import InvalidRequestError
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
)

from src.command.client.chatgpt.config import ChatGPTConfig
import src.command.client.chatgpt.callback as cbs
from src.command.client.chatgpt.types import ChatGptCallbackType

from src.command.client.chatgpt.utils import num_tokens_from_string
from src.command.client.prompt_filter.prompt_validation import (
    validate_prompt,
    check_conversation_tokens,
)

from src.common.data.reader import DataReader

DataReader = DataReader()


class ChatGptCallbackHandler:
    def __init__(self, config: ChatGPTConfig = None):
        self._config = config or ChatGPTConfig()
        self._logger = logging.getLogger(__name__)
        self._reply_request_inline_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Обратиться к специалисту", callback_data="REQUEST_COMMAND"
                    )
                ]
            ]
        )
        self._callbacks = {
            ChatGptCallbackType.START: cbs.StartCallback(self._logger, self._config)
        }

    def get_callback(self, cb_type: ChatGptCallbackType):
        return self._callbacks[cb_type]

    def generate_response(self, user_message: str, conversation: List[Dict]) -> str:
        """
        Generates a response from the ChatGPT model given the user's message and the conversation history.
    
        Args:
            user_message (str): The message sent by the user to the chatbot.
            conversation (List[Dict]): A list of dictionary objects representing the conversation history, with each
                dictionary containing "role" (the speaker) and "content" (the message content).
    
        Returns:
            str: The response generated by the ChatGPT model.
        """
        self._logger.info(f"{self.generate_response.__qualname__}")

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

    async def request(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Runs the ChatGPT service that uses the API. Handles the request after it has been checked."""
        user = update.message.from_user
        self._logger.info(f"({user.id}, {user.name}, {user.first_name}) {self.request.__qualname__}")

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
        loading_gif = await update.message.reply_video(DataReader.chatgpt.get_loading_gif())

        # First time using the chat feature
        if user_level == 0:
            context.user_data["GPT_level"] = 1
            conversation_size_check, conversation_tokens = check_conversation_tokens(
                prompt, conversation
            )
            # Check for conversation token size
            if conversation_size_check:
                print("CONVERSATION_TOKENS: ", conversation_tokens)
                # get the response
                response = self.generate_response(prompt, conversation)
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
                        conversation_tokens, self._config.model.limit_conversation_tokens
                    )
                )

        # Previously used the chat feature but still within test limit and not premium yet
        elif (
                user_level == 1
                and context.user_data["GPT_messages_sent"] < self._config.model.free_prompt_limit
                and not is_premium
        ):
            conversation_size_check, conversation_tokens = check_conversation_tokens(
                prompt, conversation
            )
            # Check for conversation token size
            if conversation_size_check:
                print("CONVERSATION_TOKENS: ", conversation_tokens)
                # get the response
                response = self.generate_response(prompt, conversation)
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
                        conversation_tokens, self._config.model.limit_conversation_tokens
                    )
                )

        # Check if user sent 5 messages but did not upgrade to premium
        elif (
                user_level == 1
                and context.user_data["GPT_messages_sent"] >= self._config.model.free_prompt_limit
                and not is_premium
        ):
            # Propose CHATGPT extension by payment at end of 5 free messages
            await update.message.reply_text(
                self._config.messages.max_messages, parse_mode=ParseMode.MARKDOWN_V2
            )

        # Check if user paid for chatgpt service
        else:
            conversation_size_check, conversation_tokens = check_conversation_tokens(
                prompt, conversation
            )
            # Check for conversation token size
            if conversation_size_check:
                # get the response
                response = self.generate_response(prompt, conversation)
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
                        conversation_tokens, self._config.model.limit_conversation_tokens
                    )
                )

    async def payment_yes(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handles user's response to pay for more interactions."""
        user = update.message.from_user
        self._logger.info(f"({user.id}, {user.name}, {user.first_name}) {self.payment_yes.__qualname__}")

        chat_id = update.message.chat_id
        title = "YaService-GPT Premium"
        description = "Увеличить длину разговора до 4096 токенов."
        # select a payload just for you to recognize its the donation from your bot
        payload = self._config.checkout_variables.extended_payload
        currency = "RUB"
        price = 100
        # price * 100 to include 2 decimal points
        prices = [LabeledPrice(self._config.checkout_variables.extended_label, price * 100)]

        await context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            os.getenv("TOKEN_PAYMENT_PROVIDER_YOOKASSA"),
            currency,
            prices,
        )

    async def precheckout_callback(
            self, update: Update, _: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Answers the PreCheckoutQuery"""
        query = update.pre_checkout_query
        # check the payload, is it from this bot and about this service?
        if query.invoice_payload == self._config.checkout_variables.extended_payload:
            print("EXTENDED_PAYLOAD: ", self._config.checkout_variables.extended_payload)
            self._logger.info(f"{self.precheckout_callback.__qualname__}")
            await query.answer(ok=True)

    async def successful_payment_callback(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle the successful payment. Set the user to Premium category and update conversation database"""
        user = update.message.from_user
        self._logger.info(
            f"({user.id}, {user.name}, {user.first_name}) {self.successful_payment_callback.__qualname__}"
        )

        context.user_data["GPT_premium"] = True
        context.user_data["GPT_premium_conversation"] = context.user_data["GPT_history"]
        context.user_data["GPT_history"] = self._config.model.conversation_init

        await update.message.reply_text("Thank you for your payment!")

    async def payment_no(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Handles user's response to not pay for more interactions."""
        user = update.message.from_user
        self._logger.info(f"({user.id}, {user.name}, {user.first_name}) {self.payment_no.__qualname__}")

        await update.message.reply_text(
            "Ваш ответ был получен. Спасибо за использование нашего сервиса!"
            "Пожалуйста, не стесняйтесь возвращаться в любое время!"
        )

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Unsets the flag in the user context that sends every incoming message from the user
        as a request to ChatGPT through the API"""
        user = update.message.from_user
        self._logger.info(f"({user.id}, {user.name}, {user.first_name}) {self.stop.__qualname__}")

        # Check if there is a chat to stop
        if context.user_data.get("GPT_active", False):
            context.user_data["GPT_active"] = False
            await update.message.reply_text(
                "YaService-GPT остановлен. "
                "Ваши сообщения больше не будут отправляться на YaService-GPT."
            )

    async def get_remaining_tokens(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Sends a message to the user with the amount of tokens he has left in his current conversation"""
        conversation_history = (
            context.user_data["GPT_premium_conversation"]
            if context.user_data["GPT_premium"]
            else context.user_data["GPT_conversation"]
        )
        conversation_tokens = sum(
            num_tokens_from_string(message["content"]) for message in conversation_history
        )
        remaining_tokens = self._config.model.limit_conversation_tokens - conversation_tokens

        await update.message.reply_text(
            f"You currently have {remaining_tokens} tokens left"
        )
