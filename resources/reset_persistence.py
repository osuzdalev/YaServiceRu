import pickle

from dotenv import load_dotenv

load_dotenv()

base_persistence = {
    "bot_data": {},
    "callback_data": ([], {}),
    "chat_data": {},
    "conversations": {},
    "user_data": {},
}

with open(constants.get("FILEPATH", "LOCAL_PERSISTENCE"), "wb") as f:
    pickle.dump(base_persistence, f)
