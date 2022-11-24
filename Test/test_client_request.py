from imports import *


@client.on(events.NewMessage(from_users=bot_id, pattern="Contacting customer service, please share your contact details"))
async def select_os(event):
    logger.info("select_os()")
    await event.click(0, share_phone=True)


if __name__ == "__main__":
    with client:
        client.start()
        client.send_message(bot_id, "/request")
        client.run_until_disconnected()
