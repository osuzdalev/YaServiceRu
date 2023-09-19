import logging
import pprint
from typing import List, Dict, Union

from sentence_transformers import SentenceTransformer
import torch
import weaviate
from numpy import ndarray
from torch import Tensor

logger_vector_db = logging.getLogger(__name__)


def get_available_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")


class VectorDatabase:
    def __init__(
        self,
        api_url: str,
        sentence_transformer: str,
        semantic_threshold: float,
        query_limit: int,
    ):
        self.client = weaviate.Client(api_url)
        self.embedding_model = SentenceTransformer(sentence_transformer)
        self.semantic_threshold = semantic_threshold
        self.query_limit = query_limit
        self.device = get_available_device()

        # Ensure the Weaviate instance is ready
        if not self.client.is_ready():
            raise Exception("Weaviate is not ready!")

    def get_schema(self) -> Dict:
        return self.client.schema.get()

    def delete_all(self) -> None:
        print(
            "Are you sure you want to delete the entire schema? This action cannot be undone. (y/n)"
        )

        confirmation = input().lower()
        if confirmation == "y":
            self.client.schema.delete_all()
            print("Entire schema deleted.")
        else:
            print("Schema not deleted.")

    def create_class(self, class_config: Dict[str, Union[str, Dict]]) -> None:
        try:
            self.client.schema.create_class(class_config)
            logger_vector_db.info(f"Class '{class_config['class']}' created.")
        except Exception as e:
            logger_vector_db.info(
                f"Error creating class '{class_config['class']}': {e}"
            )

    def delete_class(self, class_name: str) -> None:
        print(
            f"Are you sure you want to delete the '{class_name}' class? This action cannot be undone. (y/n)"
        )

        confirmation = input().lower()
        if confirmation == "y":
            self.client.schema.delete_class(class_name)
            logger_vector_db.info(f"Class '{class_name}' deleted.")
        else:
            logger_vector_db.info(f"Class '{class_name}' not deleted.")

    def write_data_object(self, data: Dict, class_name: str) -> None:
        self.client.data_object.create(data_object=data, class_name=class_name)

    def vector_query(
        self,
        collection_name: str,
        vector: Union[list[Tensor], ndarray, Tensor],
        certainty: float = 0.75,
        query_limit: int = 10,
    ) -> List[Dict[str, Union[str, float]]]:
        nearVector = {"vector": vector, "certainty": certainty}

        properties = ["content"]

        result = (
            self.client.query.get(collection_name, properties)
            .with_near_vector(nearVector)
            .with_additional(["certainty"])
            .with_limit(query_limit)
            .do()
        )

        if "errors" in result:
            raise Exception(result["errors"][0]["message"])

        return result["data_reader"]["Get"][collection_name]

    def populate_vector_database(
        self, classes: Dict[str, Dict], filters: Dict[str, List]
    ) -> None:
        # Delete all
        self.delete_all()

        # Check if the classes already exist in the schema
        schema = self.get_schema()

        for class_name, class_config in classes.items():
            if class_name not in schema:
                self.create_class(class_config)

        # Read filters from yaml and add them to Weaviate
        for filter_name, filter_lst in filters.items():
            for filter in filter_lst:
                filter_object = {"content": filter}
                self.write_data_object(filter_object, filter_name)
