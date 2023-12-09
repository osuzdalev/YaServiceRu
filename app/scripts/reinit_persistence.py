#!/usr/bin/env python3

import pickle
import os

file_path = "/Users/osuz/PycharmProjects/YaServiceRu/app/persistence/local.pkl"

if os.path.isfile(file_path):
    print(f"Removing existing {file_path}")
    os.remove(file_path)

persistent_dict = {
    "bot_data": {},
    "callback_data": ([], {}),
    "chat_data": {},
    "conversations": {},
    "user_data": {},
}

with open(file_path, "wb") as file:
    pickle.dump(persistent_dict, file)
