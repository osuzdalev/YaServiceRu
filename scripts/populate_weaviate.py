import pprint

from weaviate_client import WeaviateClient

# Connect to your Weaviate instance
weaviate_client = WeaviateClient()

# Delete all
weaviate_client.delete_all()

# Check if the Filters class already exists in the schema
schema = weaviate_client.get_schema()

if "EnglishFilters" not in schema:
    # If not, create the EnglishFilters class
    english_filter_class = {
        "class": "EnglishFilters",
        "description": "Sentences in English about our theme/business/domain to compare with incoming user prompts for filtering",
        "properties": [{"name": "content", "dataType": ["text"]}],
        "vectorizer": "text2vec-transformers",
        "moduleConfig": {
            "text2vec-transformers": {
                "poolingStrategy": "masked_mean",
                "vectorizeClassName": False,
            }
        },
    }

    weaviate_client.create_class(english_filter_class)

if "RussianFilters" not in schema:
    # If not, create the RussianFilters class
    russian_filter_class = {
        "class": "RussianFilters",
        "description": "Sentences in Russian about our theme/business/domain to compare with incoming user prompts for filtering",
        "properties": [{"name": "content", "dataType": ["text"]}],
        "vectorizer": "text2vec-transformers",
        "moduleConfig": {
            "text2vec-transformers": {
                "poolingStrategy": "masked_mean",
                "vectorizeClassName": False,
            }
        },
    }

    weaviate_client.create_class(russian_filter_class)

if "SpecialSubjectFilters" not in schema:
    # If not, create the SpecialSubjectFilters class
    special_subject_filter_class = {
        "class": "SpecialSubjectFilters",
        "description": "Sentences about particular subjects to compare with incoming user prompts, triggering a special logic/response when close enough",
        "properties": [{"name": "content", "dataType": ["text"]}],
        "vectorizer": "text2vec-transformers",
        "moduleConfig": {
            "text2vec-transformers": {
                "poolingStrategy": "masked_mean",
                "vectorizeClassName": False,
            }
        },
    }

    weaviate_client.create_class(special_subject_filter_class)

# get the schema to make sure it worked
schema = weaviate_client.get_schema()
pprint.pp(schema)


# Read filters from text files
def read_filters_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        filters = [line.strip() for line in f.readlines()]
    return filters


english_filters_file = "../data/semantic_filters_data/filters/english_filters.txt"
russian_filters_file = "../data/semantic_filters_data/filters/russian_filters.txt"

english_filters = read_filters_from_file(english_filters_file)
russian_filters = read_filters_from_file(russian_filters_file)


# Add the filters to the corresponding classes in Weaviate
for filter_text in english_filters:
    filter_object = {"content": filter_text}
    weaviate_client.write_data_object(filter_object, "EnglishFilters")

for filter_text in russian_filters:
    filter_object = {"content": filter_text}
    weaviate_client.write_data_object(filter_object, "RussianFilters")
