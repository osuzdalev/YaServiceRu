"""Basic example for a bot that can receive payment from user."""

from configparser import ConfigParser
import logging

from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import ContextTypes, CommandHandler, PreCheckoutQueryHandler, MessageHandler, filters

from resources.constants_loader import load_constants

logger_payment = logging.getLogger(__name__)

constants = load_constants()


async def start_without_shipping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an invoice without shipping-payment."""
    logger_payment.info("start_without_shipping_callback()")

    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment Example using python-telegram-bot"
    # select a payload just for you to recognize its the donation from your bot
    payload = "Custom-Payload"
    currency = "RUB"
    price = 1000
    # price * 100 to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id, title, description, payload, constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA_TEST"), currency, prices
    )


# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreCheckoutQuery"""
    logger_payment.info("precheckout_callback()")
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "Custom-Payload":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


async def successful_payment_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    logger_payment.info("successful_payment_callback()")
    await update.message.reply_text("Thank you for your payment!")


pay_handler = CommandHandler("pay", start_without_shipping_callback)
precheckout_handler = PreCheckoutQueryHandler(precheckout_callback)
successful_payment_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
