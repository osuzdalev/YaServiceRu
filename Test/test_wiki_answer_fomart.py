from imports import *
from Utils.answer_markdown import test

if __name__ == "__main__":

    with client:
        client.start()
        client.send_message(bot_id, test, parse_mode='markdown')
