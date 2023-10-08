import inspect
import json
import logging
from typing import List, Dict, Union

from sentence_transformers import SentenceTransformer
import torch
import weaviate
from weaviate.util import generate_uuid5
from numpy import ndarray
from torch import Tensor

from yaserviceru.app.data_reader import VectorDatabaseReader

logger_vector_db = logging.getLogger(__name__)


def get_available_device():
    logger_vector_db.info(f"{inspect.currentframe().f_code.co_name}")
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
        self.classes = {}
        self.device = get_available_device()
        self.vector_database_data_reader = VectorDatabaseReader()

        # Ensure the vector_db_client instance is ready
        if not self.vector_db_client.is_ready():
            raise Exception("vector_db_client is not ready!")

        self.populate_vector_database(
            self.vector_database_data_reader.get_classes(),
            self.vector_database_data_reader.get_filters(),
        )

    def populate_vector_database(
        self, classes: Dict[str, Dict], filters: Dict[str, Dict]
    ) -> None:
        """
        Populate the vector database with specified classes and filters.

        This method reinitializes the vector database with given classes if they don't already exist, then writes
        provided filters to the database. Each class and filter is validated before being added. If an error occurs
        during the process, it raises an exception and logs an error message.

        Parameters: - classes (Dict[str, Dict]): A dictionary of class names and their configurations to be added to
        the vector database. - filters (Dict[str, List]): A dictionary containing filter names and lists of filter
        strings to be added to the corresponding classes in the vector database.

        Raises:
        - ValueError: If a filter object fails the validation.
        - AssertionError: If no objects are found in the vector database after writing.

        Logs: - Informational messages tracking the progress of the database population process, including classes
        and filters added.
        """

        logger_vector_db.info(
            f"Populating vector database - {inspect.currentframe().f_code.co_name}"
        )

        # Check if classes already exist
        if self.check_classes(classes):
            logger_vector_db.info("Classes already exist. Skipping population.")
            return

        logger_vector_db.info("Reinitialising vector database")
        self.classes = classes
        self.delete_all()

        # Print classes to be written to vector_db
        logger_vector_db.info("Classes to be written to vector_db:")
        for class_name, class_config in self.classes.items():
            logger_vector_db.info(f"{class_name}")

        # Create the classes in the vector_db
        schema = self.get_schema()
        for class_name, class_config in self.classes.items():
            if class_name not in schema:
                self.create_class(class_config)
                logger_vector_db.info(f"Class '{class_name}' created")

        # Log updated schema
        logger_vector_db.info(f"Updated Schema: {self.get_schema()}")

        logger_vector_db.info("Writing filters to vector database...")

        # Read filters from the provided dictionary and add them to vector_db
        for filter_name, filter_lst in filters.items():
            for filter_str in filter_lst:
                filter_object = {"content": filter_str}

                # Validate the filter object before writing to vector_db
                valid_filter_object = self.vector_db_client.data_object.validate(
                    data_object=filter_object,
                    class_name=filter_name,
                    uuid=generate_uuid5(filter_object),
                )

                # Log validation errors if any, else write data object to vector_db
                if not valid_filter_object["valid"]:
                    logger_vector_db.error(
                        json.dumps(valid_filter_object["error"], indent=2)
                    )
                    raise ValueError("Vector Database object format not valid")

                self.write_data_object(filter_object, filter_name)
                logger_vector_db.info(
                    f"Filter '{filter_str}' added to class '{filter_name}'"
                )

            # Ensure objects are written properly
            if not self.get_all_objects_from_class(self.classes):
                raise AssertionError(
                    "No objects found in vector database after writing"
                )

        logger_vector_db.info("Vector database populated successfully")

    def vector_query(
        self,
        collection_name: str,
        vector: Union[list[Tensor], ndarray, Tensor],
        certainty: float = 0.75,
        query_limit: int = 10,
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Execute a vector query on the specified collection and return the results.

        This method performs a vector similarity search in the given collection, using the provided vector, certainty threshold, and query limit. Results include items that meet the certainty criteria up to the specified limit.

        Parameters:
        - collection_name (str): The name of the collection to query.
        - vector (Union[list[Tensor], ndarray, Tensor]): The vector used for similarity search.
        - certainty (float, optional): The threshold for result inclusion, defaults to 0.75.
        - query_limit (int, optional): The maximum number of results to return, defaults to 10.

        Returns:
        - List[Dict[str, Union[str, float]]]: A list of dictionaries containing the query results, each including content and certainty values.

        Raises:
        - Exception: If an error occurs during the query execution.
        """
        logger_vector_db.info(f"{inspect.currentframe().f_code.co_name}")

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
        logger_vector_db.info(f"{inspect.currentframe().f_code.co_name}")

        try:
            self.vector_db_client.schema.create_class(class_config)
            logger_vector_db.info(f"Class '{class_config['class']}' created.")
        except Exception as e:
            logger_vector_db.info(
                f"Error creating class '{class_config['class']}': {e}"
            )

    def check_classes(self, classes) -> bool:
        """
        Check if the specified classes exist in the vector database.

        Iterates over the provided 'classes' dictionary to verify the existence of each class in the vector database. If all classes are found, it sets the 'classes' attribute and returns True. If any class is missing, it returns False.

        Parameters:
        - classes (dict): Dictionary of class names and their configurations.

        Returns:
        - bool: True if all classes are in the vector database, False otherwise.

        Logs:
        - Informational messages about the presence or absence of classes.
        """
        logger_vector_db.info(f"{inspect.currentframe().f_code.co_name}")

        for class_name, configs in classes.items():
            try:
                self.vector_db_client.schema.get(class_name)
                logger_vector_db.info(f"Class {class_name} in vector database")
            except weaviate.exceptions.UnexpectedStatusCodeException:
                logger_vector_db.info(
                    f"Class {class_name} not found in vector database"
                )
                return False

        # Since all classes are correct assign them as attribute for this launch
        self.classes = classes

        return True

    def get_all_objects_from_class(self, class_name, batch_size=20):
        """
        Retrieve all objects from a Weaviate schema class.

        Parameters:
            class_name: The name of the class from which to retrieve objects.
            batch_size: The number of objects to retrieve per batch.

        Returns:
            A list of all objects in the specified class.
        """
        all_objects = []
        cursor = None

        while True:
            query = (
                self.vector_db_client.query.get(class_name)
                .with_additional(["id vector"])
                .with_limit(batch_size)
            )

            if cursor is not None:
                query = query.with_after(cursor)

            results = query.do()

            objects = results["data"]["Get"][class_name]
            if len(objects) == 0:
                break

            all_objects.extend(objects)
            cursor = objects[-1]["_additional"]["id"]

        logger_vector_db.info(f"All objects from {class_name}:")
        logger_vector_db.info(all_objects)

        return all_objects

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
            data_object=data, class_name=class_name, uuid=generate_uuid5(data)
        )
