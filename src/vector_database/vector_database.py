import inspect
import json
import logging
from pprint import pprint
from typing import List, Dict, Union

from sentence_transformers import SentenceTransformer
import torch
import weaviate
from numpy import ndarray
from torch import Tensor

logger_vector_db = logging.getLogger(__name__)


def get_available_device():
    logger_vector_db.info(
        f"{inspect.currentframe().f_code.co_name}"
    )
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
        self.vector_db_client = weaviate.Client(api_url)
        self.embedding_model = SentenceTransformer(sentence_transformer)
        self.semantic_threshold = semantic_threshold
        self.query_limit = query_limit
        self.device = get_available_device()

        # Ensure the vector_db_client instance is ready
        if not self.vector_db_client.is_ready():
            raise Exception("vector_db_client is not ready!")

    def populate_vector_database(
        self, classes: Dict[str, Dict], filters: Dict[str, List]
    ) -> None:
        logger_vector_db.info(
            f"{inspect.currentframe().f_code.co_name}"
        )

        self.delete_all()
        schema = self.get_schema()

        print("classes to be written to vector_db")
        pprint(classes.items())

        for class_name, class_config in classes.items():
            if class_name not in schema:
                self.create_class(class_config)

        # Read filters from yaml and add them to vector_db
        for filter_name, filter_lst in filters.items():
            for filter_str in filter_lst:
                filter_object = {"content": filter_str}
                self.write_data_object(filter_object, filter_name)

        # get the schema
        schema = self.get_schema()

        # print the schema
        pprint(schema)

    def vector_query(
        self,
        collection_name: str,
        vector: Union[list[Tensor], ndarray, Tensor],
        certainty: float = 0.75,
        query_limit: int = 10,
    ) -> List[Dict[str, Union[str, float]]]:
        logger_vector_db.info(
            f"{inspect.currentframe().f_code.co_name}"
        )

        nearVector = {"vector": vector, "certainty": certainty}

        properties = ["content"]

        result = (
            self.vector_db_client.query.get(collection_name, properties)
            .with_near_vector(nearVector)
            .with_additional(["certainty"])
            .with_limit(query_limit)
            .do()
        )

        print(json.dumps(result, indent=4))

        if "errors" in result:
            raise Exception(result["errors"][0]["message"])

        return result["data"]["Get"][collection_name]

    def create_class(self, class_config: Dict[str, Union[str, Dict]]) -> None:
        logger_vector_db.info(
            f"{inspect.currentframe().f_code.co_name}"
        )

        try:
            self.vector_db_client.schema.create_class(class_config)
            logger_vector_db.info(f"Class '{class_config['class']}' created.")
        except Exception as e:
            logger_vector_db.info(
                f"Error creating class '{class_config['class']}': {e}"
            )

    def get_schema(self) -> Dict:
        return self.vector_db_client.schema.get()

    def delete_all(self) -> None:
        self.vector_db_client.schema.delete_all()
        print("Entire schema deleted.")

    def delete_class(self, class_name: str) -> None:
        self.vector_db_client.schema.delete_class(class_name)
        logger_vector_db.info(f"Class '{class_name}' deleted.")

    def write_data_object(self, data: Dict, class_name: str) -> None:
        self.vector_db_client.data_object.create(
            data_object=data, class_name=class_name
        )
