import logging
import pprint
from typing import List, Dict, Union

import weaviate
from numpy import ndarray
from torch import Tensor

from resources.constants_loader import load_constants

logger_weaviate = logging.getLogger(__name__)
constants = load_constants()


class WeaviateClient:
    def __init__(self, api_url: str = constants.get("API", "WEAVIATE")):
        self.client = weaviate.Client(api_url)

        # Ensure the Weaviate instance is ready
        if not self.client.is_ready():
            raise Exception("Weaviate is not ready!")

    def get_schema(self) -> Dict:
        return self.client.schema.get()

    def delete_all(self) -> None:
        print("Are you sure you want to delete the entire schema? This action cannot be undone. (y/n)")

        confirmation = input().lower()
        if confirmation == 'y':
            self.client.schema.delete_all()
            print("Entire schema deleted.")
        else:
            print("Schema not deleted.")

    def create_class(self, class_config: Dict[str, Union[str, Dict]]) -> None:
        try:
            self.client.schema.create_class(class_config)
            logger_weaviate.info(f"Class '{class_config['class']}' created.")
        except Exception as e:
            logger_weaviate.info(f"Error creating class '{class_config['class']}': {e}")

    def delete_class(self, class_name: str) -> None:
        print(f"Are you sure you want to delete the '{class_name}' class? This action cannot be undone. (y/n)")

        confirmation = input().lower()
        if confirmation == 'y':
            self.client.schema.delete_class(class_name)
            logger_weaviate.info(f"Class '{class_name}' deleted.")
        else:
            logger_weaviate.info(f"Class '{class_name}' not deleted.")

    def write_data_object(self, data: Dict, class_name: str) -> None:
        self.client.data_object.create(data_object=data, class_name=class_name)

    def vector_query(self, collection_name: str, vector: Union[list[Tensor], ndarray, Tensor], certainty: float = 0.7, query_limit: int = 10) -> List[Dict[str, Union[str, float]]]:
        nearVector = {
            "vector": vector,
            "certainty": certainty
        }

        properties = [
            "content"
        ]

        result = (
            self.client.query
            .get(collection_name, properties)
            .with_near_vector(nearVector)
            .with_additional(["certainty"])
            .with_limit(query_limit)
            .do()
        )

        if "errors" in result:
            raise Exception(result["errors"][0]['message'])

        return result["data"]["Get"][collection_name]

