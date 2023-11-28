from contextlib import closing

import os
from loguru import logger
from pprint import pformat

import psycopg

from typing import List, Tuple


# TODO Investigate using the database modeling library to interact with the database
# See, for example, django: https://docs.djangoproject.com/en/4.2/topics/db/
# other option: framework sql alchemy
# asyncpg


def create_db_connection(db_auth):
    return psycopg.connect(**db_auth)


def insert_new_user(
    user_id: int, user_name: str, first_name: str, last_name: str, db_auth: dict
) -> None:
    """
    Inserts a new user into the database if the user does not already exist.

    This function checks if a user with the provided user_id already exists in the database.
    If the user does not exist, it inserts the new user with the provided information into the users table.
    If the user already exists, a debug log message is recorded.

    Parameters:
    - user_id : int : The unique identifier of the user.
    - user_name : str : The username of the user.
    - first_name : str : The first name of the user.
    - last_name : str : The last name of the user.
    - db_auth : dict : The database authentication credentials.

    Returns:
    - None

    Raises:
    - psycopg.Error: Raised when there is an error executing the database commands.
    """
    logger.info(f" ")
    try:
        with create_db_connection(db_auth) as conn:
            cursor = conn.cursor()
            result = cursor.execute(
                "select * from users where user_id = %s", (user_id,)
            )
            if result.fetchone() is None:
                cursor.execute(
                    "insert into users (user_id, user_name, first_name, last_name) values (%s, %s, %s, %s);",
                    (user_id, user_name, first_name, last_name),
                )
                conn.commit()
            else:
                logger.debug("Customer already in Database")
    except psycopg.Error as e:
        logger.error(e)


def get_user_data(user_id: int, db_auth: dict) -> None:
    """Stuff"""
    logger.info(f" ")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from users where user_id = %s", (user_id,))
        return result.fetchone()


def insert_user_phone_number(user_id: int, phone_number: int, db_auth: dict) -> None:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "update users set phone_number = %s where user_id = %s;",
            (phone_number, user_id),
        )
        conn.commit()
        logger.info("Phone number added into Database")


def get_customer_data(user_id: int, db_auth: dict) -> List:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select users.user_id, users.user_name, users.first_name, users.last_name,"
            "users.phone_number, users.join_date, "
            "customers.warning "
            "from users, customers "
            "where user_id = %s and customer_id = %s",
            (
                user_id,
                user_id,
            ),
        )

        return result.fetchone()


def get_customer_last_order_id(user_id: int, contractor_id: int, db_auth: dict) -> int:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where (customer_id = %s and contractor_id = %s)",
            (user_id, contractor_id),
        )
        orders = result.fetchall()
        logger.debug(f"orders: {orders}")

        return orders[-1][0]


def insert_new_order(
    user_id: int, device_context: List, default_contractor_id: int, db_auth: dict
) -> None:
    logger.debug(f)

    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()

        # Check the length of device_context and assign default values if necessary
        os = device_context[0] if len(device_context) > 0 else None
        device = device_context[1] if len(device_context) > 1 else None
        category = device_context[2] if len(device_context) > 2 else None
        problem = device_context[-1] if len(device_context) > 3 else None

        cursor.execute(
            "insert into orders (customer_id, contractor_id, os, device, category, problem) "
            "values (%s, %s, %s, %s, %s, %s);",
            (user_id, default_contractor_id, os, device, category, problem),
        )
        conn.commit()


def get_order_data(order_id: int, db_auth: dict) -> List:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from orders where order_id = %s", (order_id,))

        return result.fetchone()


def get_open_orders(db_auth: dict) -> List[Tuple]:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where completed = 0 and contractor_id is null"
        )
        return result.fetchall()


def get_assigned_orders(db_auth: dict) -> List[Tuple]:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where completed = 0 and contractor_id is not null"
        )
        return result.fetchall()


def update_order_Complete(order_id: int, timestamp: str, db_auth: dict) -> None:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "update orders set completed = %s, completed_date = %s where order_id = %s",
            (1, timestamp, order_id),
        )
        conn.commit()


def get_contractor_data(user_id: int, db_auth: dict) -> List:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select users.user_id, users.user_name, users.first_name, users.last_name, users.phone_number, users.join_date, "
            "contractors.warning "
            "from users, contractors "
            "where user_id = %s and contractor_id = %s",  # TODO: numbered pass
            (
                user_id,
                user_id,
            ),
        )

        return result.fetchone()


def get_all_contractor_id(db_auth: dict) -> List:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select contractor_id from contractors")
        contractor_ids = [i[0] for i in result.fetchall()]

        return contractor_ids


def update_order_contractor_id(
    order_id: int, new_contractor_id: int, db_auth: dict
) -> None:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "update orders set contractor_id = %s where order_id = %s",
            (new_contractor_id, order_id),
        )
        conn.commit()


def insert_assign(
    old_contractor_id: int, order_id: int, new_contractor_id: int, db_auth: dict
) -> None:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "insert into assign (old_contractor_id, order_id, new_contractor_id) "
            "values (%s, %s, %s);",
            (old_contractor_id, order_id, new_contractor_id),
        )
        conn.commit()


def check_assign(
    old_contractor_id: int, order_id: int, new_contractor_id: int, db_auth: dict
) -> bool:
    logger.debug(f)
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from assign where old_contractor_id = %s and order_id = %s and new_contractor_id = %s",
            (old_contractor_id, order_id, new_contractor_id),
        )

        return bool(result.fetchone())


def insert_message(message_id: int, user_id: int, text: str, db_auth: dict) -> None:
    """
    Inserts a message into the database.

    This function handles the insertion of messages into the database called by the "data_collection" handler,
    it also handles UniqueViolation error by incrementing the message_id and retries the insertion.

    Parameters:
    - message_id : int : The ID of the message.
    - user_id : int : The ID of the user who sent the message.
    - text : str : The text content of the message.
    - db_auth : dict : The database authentication credentials.

    Returns:
    - None

    Raises:
    - psycopg2.errors.UniqueViolation: Raised when a unique violation error occurs during insertion.
    - Exception: Raised for unexpected errors during insertion.
    """

    if (
        not isinstance(message_id, int)
        or not isinstance(user_id, int)
        or not isinstance(text, str)
    ):
        logger.error("Invalid parameters")
        return

    logger.debug(" ")
    logger.debug(f"inserting: {message_id}, {user_id}, {text}")

    with closing(create_db_connection(db_auth)) as conn:
        cursor = conn.cursor()

        try:
            # Try to insert the message
            cursor.execute(
                "insert into messages (message_id, user_id, message_text) values (%s, %s, %s)",
                (message_id, user_id, text),
            )
            # If successful, commit the transaction
            conn.commit()
        # TODO: Needs to handle InlineButton Callbacks that send a new message using the same message_id
        # this hotfix works for now but needs to be improved
        except psycopg.errors.UniqueViolation:
            # Rollback the transaction
            conn.rollback()

            # Increment the message_id
            message_id += 1
            logger.debug(
                f"UniqueViolation occurred. Retrying with incremented message_id {message_id}"
            )

            # Try to insert the message again
            try:
                cursor.execute(
                    "insert into messages (message_id, user_id, message_text) values (%s, %s, %s)",
                    (message_id, user_id, text),
                )
                # Commit the transaction
                conn.commit()
            except Exception as ex:
                # Handle or log any exception that occurred in the second attempt
                logger.debug(f"An error occurred during retry: {ex}")

        except Exception as ex:
            # Handle or log any other exception
            logger.debug(f"An unexpected error occurred: {ex}")
            conn.rollback()
