from imports import *
from Utils.answer_markdown import test

with open("../Utils/test.yaml", mode="rb") as fp:
    config = yaml.load(fp, Loader=Loader)

yaml_test = config["text"]
print(yaml_test)

if __name__ == "__main__":
    with client:
        client.start()
        client.send_message(bot_id, yaml_test, parse_mode="markdown")
