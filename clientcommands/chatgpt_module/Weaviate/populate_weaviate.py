import pprint

from weaviate_client import WeaviateClient

# Connect to your Weaviate instance
weaviate_client = WeaviateClient()

# Delete all
weaviate_client.delete_all()

# Check if the Filters class already exists in the schema
schema = weaviate_client.get_schema()
if "Filters" not in schema:
    # If not, create the Filters class
    filter_schema = {
        "class": "Filters",
        "description": "Sentences with which the incoming user prompt message will be compared "
                       "to determine if the bot should respond",
        "properties": [{
            "name": "content",
            "dataType": ["text"]
        }],
        "vectorizer": "text2vec-transformers",
        "moduleConfig": {
            "text2vec-transformers": {
                "poolingStrategy": "masked_mean",
                "vectorizeClassName": False
            }
        },
    }

    weaviate_client.create_class(filter_schema)

# get the schema to make sure it worked
schema = weaviate_client.get_schema()
pprint.pp(schema)

# Example filters
filters = [
    "I have a problem with my electronic device and need your help to fix it",
    "My computer is not working properly, can you assist me?",
    "My phone is acting weird, can you help me resolve the issue?",
    "I'm having trouble with my tablet, can you guide me on how to fix it?",
    "У меня проблема с моим электронным устройством, и мне нужна ваша помощь, чтобы исправить это",
    "Мой компьютер не работает должным образом, вы можете мне помочь?",
    "Мой телефон ведет себя странно, можете помочь мне решить проблему?",
    "У меня проблемы с моим планшетом, не могли бы вы помочь мне в исправлении?"
]

# Add the filters to the Filters class in Weaviate
for filter_text in filters:
    filter_object = {"content": filter_text}
    weaviate_client.write_data_object(filter_object, "Filters")
