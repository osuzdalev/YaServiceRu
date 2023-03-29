import pickle
import os

from resources.constants_loader import load_constants

constants = load_constants()
file_path = constants.get("FILEPATH", "LOCAL_PERSISTENCE")

if os.path.isfile(file_path):
    os.remove(file_path)
else:
    print(f"{file_path} not found.")

persistent_dict = {'bot_data': {},
                   'callback_data': ([], {}),
                   'chat_data': {},
                   'conversations': {},
                   'user_data': {}
                   }

with open(file_path, 'wb') as file:
    pickle.dump(persistent_dict, file)
