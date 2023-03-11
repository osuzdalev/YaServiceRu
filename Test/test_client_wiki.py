from imports import *


@client.on(events.NewMessage(from_users=bot_id, pattern="Select a Brand/OS"))
async def select_os(event):
    logger.info("select_os()")
    await event.click(0, 0)


# @client.on(events.MessageEdited(from_users=bot_id, pattern="Select a device"))
# async def select_device(event):
#     logger.info("select_device()")
#     await event.click(0)
#
#
# @client.on(events.MessageEdited(from_users=bot_id, pattern="Select a category"))
# async def select_component(event):
#     logger.info("select_component()")
#     await event.click(0)
#
#
# @client.on(events.MessageEdited(from_users=bot_id, pattern="Select a problem"))
# async def select_problem(event):
#     logger.info("select_problem()")
#     await event.click(0)


if __name__ == "__main__":
    with client:
        client.start()
        #client.send_message(bot_id, "/start")
        client.send_message(bot_id, "/wiki")
        client.run_until_disconnected()
