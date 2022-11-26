from imports import *


@client.on(events.NewMessage(from_users=bot_id, pattern="Select Contractor"))
async def select_contractor_1(event):
    logger.info("select_contractor_1()")
    await event.click(1, 0)


@client.on(events.MessageEdited(from_users=bot_id, pattern="Select Contractor"))
async def select_contractor_2(event):
    logger.info("select_contractor_2()")
    await event.click(0, 1)


if __name__ == "__main__":
    with client:
        client.start()
        client.send_message(bot_id, "/forward 20")
        client.run_until_disconnected()
