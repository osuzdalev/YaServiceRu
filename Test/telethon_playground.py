from imports import *


async def main():
    async for message in client.iter_messages('me'):
        # You can download media from messages, too!
        # The method will return the path where the file was saved.
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # printed after download is done

    # Disconnect the client
    client.disconnect()

if __name__ == '__main__':
    client.start()
    with client:
        client.loop.run_until_complete(main())
