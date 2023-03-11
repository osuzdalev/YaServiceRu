from imports import *


@client.on(events.NewMessage(from_users=bot_id, pattern="Select a Brand/OS"))
async def select_os(event):
    logger.info("select_os()")
    await event.click(0, 0)


@client.on(events.MessageEdited(from_users=bot_id, pattern="Select a device"))
async def select_device(event):
    logger.info("select_device()")
    await event.click(0)


@client.on(events.MessageEdited(from_users=bot_id, pattern="Mac"))
async def select_component(event):
    logger.info("Mac")
    await event.click(0)


@client.on(events.MessageEdited(from_users=bot_id, pattern="Slowing / Bugging"))
async def select_problem(event):
    logger.info("Slowing / Bugging")
    await event.click(0)


@client.on(events.MessageEdited(from_users=bot_id, pattern="TEST"))
async def select_problem(event):
    logger.info("TEST")
    await event.click(0)


if __name__ == "__main__":
    with client:
        client.start()
        #client.send_message(bot_id, "/start")
        client.send_message(bot_id, "/wiki")
        client.run_until_disconnected()
