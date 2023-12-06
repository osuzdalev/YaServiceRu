from typing import Any, List, Tuple

from loguru import logger

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an Inline message to confirm the call"""
    user = update.effective_user
    logger.info(f"({user.id}, {user.name}, {user.first_name})")
    context.user_data.setdefault("Request_temp_messages", [])
    keyboard = [
        [
            InlineKeyboardButton("❌Отменить", callback_data="REQUEST_CALL_CANCEL"),
            InlineKeyboardButton("✅Подтвердить", callback_data="REQUEST_CALL_CONFIRM"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    temp_message = await context.bot.sendMessage(
        update.effective_chat.id,
        "Подтвердить вызов специалиста?",
        reply_markup=reply_markup,
    )
    context.user_data["Request_temp_messages"].append(temp_message)


async def confirm_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """sends a request (a message with all relevant/context information) to Customer Service"""
    query = update.callback_query
    user = query.from_user
    user_data = [user.id, user.name, user.first_name, user.last_name]
    logger.info(f"({user.id}, {user.name}, {user.first_name})")

    device_context = context.user_data.get("Device_Context", [])

    # tldb.insert_new_order(user.id, device_context)

    # OrderID = tldb.get_customer_last_OrderID(user.id)
    order_message_str = get_order_message_str(0000, user_data, device_context)

    await context.bot.sendMessage(
        context.bot_data["config"]["telefix"]["contact"]["tg_id"]["dev"],
        order_message_str,
    )
    await query.answer(text="Служба поддержки свяжется с вами.", show_alert=True)

    # cleaning
    for message in context.user_data["Request_temp_messages"]:
        await message.delete()
        context.user_data["Request_temp_messages"] = []


def get_order_message_str(
    order_id: int, user_data: Any, device_context: Any, phone_number: int = None
) -> str:
    """Creates a nice string with all the relevant database of an Order to be sent as a message to Contractor"""
    logger.info(" ")
    user_info = ""
    if isinstance(user_data, List):
        user_info = [
            user_data[1],
            user_data[2],
            user_data[3],
            str(phone_number),
            f"id:{user_data[0]}",
        ]
        user_info = "\n".join(user_info)
    elif isinstance(user_data, Tuple):
        user_info = (
            f"@{user_data[1]}"
            + "\n"
            + user_data[2]
            + "\n"
            + user_data[3]
            + "\n"
            + str(phone_number)
            + "\n"
            + "id:"
            + str(user_data[0])
        )

    device_info = "\n".join(device_context)
    logger.debug(f"device_context: {device_context}")

    return "\n\n".join(
        [
            "Customer service required",
            f"Order# {order_id}",
            user_info,
            device_info,
        ]
    )


async def cancel_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Cancel the request and remove all the related temp messages sent"""
    query = update.callback_query
    try:
        user = query.from_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")
    except AttributeError:
        user = update.effective_user
        logger.info(f"({user.id}, {user.name}, {user.first_name})")

    # cleaning
    for message in context.user_data["Request_temp_messages"]:
        await message.delete()
        context.user_data["Request_temp_messages"] = []
