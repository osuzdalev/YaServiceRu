import json
import sys
from pprint import pformat
from typing import List, Dict, Union

from loguru import logger

from numpy import ndarray
import torch
from torch import Tensor
from sentence_transformers import SentenceTransformer
import weaviate
from weaviate.util import generate_uuid5

from ..common.types import StdModuleType
from ..core.config_template import ClassConfig


def get_available_device():
    logger.info(" ")
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        logger.info("Torch using MPS")
        return torch.device("mps")
    else:
        logger.info("Torch using CPU")
        return torch.device("cpu")


class VectorDatabase:
    """
    Manages a vector database using Weaviate, a vector search engine, for semantic search and retrieval.

    This class is designed to handle the initialization, population, and querying of a vector database. It uses
    Weaviate to store and retrieve data objects based on semantic similarity. The class also integrates sentence
    transformers for vector representation of textual data and utilizes the most suitable computing device available
    (CPU, CUDA, MPS).

    This class is essential for applications involving semantic search and retrieval, such as chatbots or recommendation systems.

    Attributes:
        vector_db_client (weaviate.Client): Client for interacting with Weaviate database.
        embedding_model (SentenceTransformer): Model for generating sentence data.
        semantic_threshold (float): Threshold for semantic similarity in queries.
        query_limit (int): Limit for the number of results returned in queries.
        classes (dict): Dictionary of classes (schema definitions) in the database.
        device (torch.device): The computational device used for model operations.

    Methods:
        populate_vector_database(classes, filters): Populates the database with classes and filters.
        vector_query(collection_name, vector, certainty, query_limit): Performs a vector similarity search.
        create_class(class_config): Creates a new class in the vector database schema.
        check_classes(classes): Checks if specified classes exist in the vector database.
        get_all_objects_from_class(class_name, batch_size): Retrieves all objects from a specified class.
        get_schema(): Retrieves the current schema of the vector database.
        delete_all(): Deletes all classes and objects in the database.
        delete_class(class_name): Deletes a specific class from the database.
        write_data_object(data, class_name): Writes a data object to a specific class in the database.
    """

    TYPE = StdModuleType.VECTOR_DATABASE

    def __init__(
        self,
        api_url: str,
        sentence_transformer: str,
        semantic_threshold: float,
        query_limit: int,
        classes_config: dict[str, ClassConfig],
        filters_config: Dict[str, List[str]],
    ):
        try:
            logger.info("Connecting to vector database client...")
            self.vector_db_client = weaviate.Client(api_url)
        except Exception as e:
            logger.exception(f"Failed to initialize Weaviate client: {e}")
            sys.exit(1)
        try:
            self.embedding_model = SentenceTransformer(sentence_transformer)
        except Exception as e:
            logger.exception(f"Failed to load SentenceTransformer model: {e}")
            sys.exit(1)

        self.semantic_threshold = semantic_threshold
        self.query_limit = query_limit
        self.classes = {}
        self.device = get_available_device()

        try:
            self.populate_vector_database(classes_config, filters_config)
        except Exception as e:
            logger.exception(f"Error while populating vector database: {e}")
            sys.exit(1)

    def populate_vector_database(
            self, classes_config: dict[str, ClassConfig], filters_config: Dict[str, List[str]]
    ) -> None:
        """
        Populate the vector database with specified classes and filters.

        This method reinitializes the vector database with given classes if they don't already exist, then writes
        provided filters to the database. Each class and filter is validated before being added. If an error occurs
        during the process, it raises an exception and logs an error message.

        Parameters:
            - classes (Dict[str, Dict]): A dictionary of class names and their configurations to be added to
            the vector database.
            - filters (Dict[str, List]): A dictionary containing filter names and lists of filter
            strings to be added to the corresponding classes in the vector database.

        Raises:
            - ValueError: If a filter object fails the validation.
            - AssertionError: If no objects are found in the vector database after writing.
        """

        logger.info(" ")

        # FIXME

        # Check if classes already exist
        if self.check_classes(classes_config):
            logger.info("Classes already exist. Skipping population.")
            return

        logger.info("Reinitialising vector database")
        self.classes = classes_config
        self.delete_all()

        # Print classes to be written to vector_db
        logger.info("Classes to be written to vector_db:")
        for class_name in self.classes:
            logger.info(f"{class_name}")

        # Create the classes in the vector_db
        for class_name, class_config in self.classes.items():
            self.create_class(class_config)
            logger.info(f"Class '{class_name}' created")

        # Log updated schema
        logger.info(f"Updated Schema: {pformat(self.get_schema())}")

        logger.info("Writing filters to vector database...")

        # Read filters from the provided dictionary and add them to vector_db
        for filter_name, filter_lst in filters_config.items():
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
                    logger.error(json.dumps(valid_filter_object["error"], indent=2))
                    raise ValueError("Vector Database object format not valid")

                self.write_data_object(filter_object, filter_name)
                logger.info(f"Filter '{filter_str}' added to class '{filter_name}'")

            # Ensure objects are written properly
            if not self.get_all_objects_from_class(filter_name):
                raise AssertionError(
                    "No objects found in vector database after writing"
                )

        logger.info("Vector database populated successfully")

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
        logger.info(" ")

        nearVector = {"vector": vector, "certainty": certainty}

        properties = ["content"]

        result = (
            self.vector_db_client.query.get(collection_name, properties)
            .with_near_vector(nearVector)
            .with_additional(["certainty"])
            .with_limit(query_limit)
            .do()
        )

        try:
            max_certainty = result["data"]["Get"][collection_name][0]["_additional"][
                "certainty"
            ]
            content = result["data"]["Get"][collection_name][0]["content"]
            logger.info(f"Max certainty: {max_certainty}\nContent: {content}")
        except IndexError:
            logger.warning("Semantic query yielded NULL")

        if "errors" in result:
            raise RuntimeError(result["errors"][0]["message"])

        return result["data"]["Get"][collection_name]

    def create_class(self, class_config: ClassConfig) -> None:
        logger.info(" ")

        try:
            self.vector_db_client.schema.create_class(class_config)
            logger.info(f"Class '{class_config['class_name']}' created.")
        except Exception as e:
            logger.info(f"Error creating class '{class_config['class_name']}': {e}")

    # TODO did not return "False" when data were empty (the volumes was not properly mounted).
    # check why it could not tell the database was empty, there was no schema, and yet still thought everything was ok.
    def check_classes(self, classes) -> bool:
        """
        Check if the specified classes exist in the vector database.

        Iterates over the provided 'classes' dictionary to verify the existence of each class in the vector database. If all classes are found, it sets the 'classes' attribute and returns True. If any class is missing, it returns False.

        Parameters:
        - classes (dict): Dictionary of class names and their configurations.

        Returns:
        - bool: True if all classes are in the vector database, False otherwise.
        """
        logger.info(" ")

        for class_name, configs in classes.items():
            try:
                self.vector_db_client.schema.get(class_name)
                logger.info(f"Class {class_name} in vector database")
            except weaviate.exceptions.UnexpectedStatusCodeException:
                logger.info(f"Class {class_name} not found in vector database")
                return False

        # FIXME this checks only if there are objects. Not if every class is filled.
        try:
            obj = self.vector_db_client.data_object.get()
            logger.info(f"Objects found in vector_db: {obj['totalResults']}")
        except Exception as e:
            logger.info(f"Checking objects yielded the following error {e}")
            return False

        # TODO if everything is fine in the schema then its classes
        # should be the ones used for the objects attributes, not the ones
        # from the config file
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

        logger.info(f"All objects from {class_name}:")
        logger.info(all_objects)

        return all_objects

    # TODO implement backup method
    def backup(self):
        """
        If you check the contents of the backup directory again,
        you should see a new directory called my-very-first-backup
        containing the backup data files.
        """
        backup = self.vector_db_client.backup.create(
            backup_id="my-very-first-backup",
            backend="filesystem",
        )

        return self.vector_db_client.backup.get_create_status(
            backup_id="my-very-first-backup",
            backend="filesystem",
        )

    # TODO implement restore method
    def restore(self):
        result = self.vector_db_client.backup.restore(
            backup_id="my-very-first-backup",
            backend="filesystem",
        )

    def get_schema(self) -> Dict:
        return self.vector_db_client.schema.get()

    def delete_all(self) -> None:
        self.vector_db_client.schema.delete_all()
        logger.info("Entire schema deleted.")

    def delete_class(self, class_name: str) -> None:
        self.vector_db_client.schema.delete_class(class_name)
        logger.info(f"Class '{class_name}' deleted.")

    def write_data_object(self, data: Dict, class_name: str) -> None:
        self.vector_db_client.data_object.create(
            data_object=data, class_name=class_name, uuid=generate_uuid5(data)
        )
