import pickle

from resources.constants_loader import load_constants

constants = load_constants()

base_persistence = {'bot_data': {},
                    'callback_data': ([], {}),
                    'chat_data': {},
                    'conversations': {},
                    'user_data': {}
                    }

with open(constants.get("FILEPATH", "LOCAL_PERSISTENCE"), "wb") as f:
    pickle.dump(base_persistence, f)
