import os
import logging
from pprint import pprint

import psycopg

from typing import List, Tuple

logger_tl_db = logging.getLogger(__name__)


def create_db_connection(db_auth):
    return psycopg.connect(**db_auth)


def insert_new_user(
    user_id: int, user_name: str, first_name: str, last_name: str, db_auth: dict
) -> None:
    """Stuff"""
    logger_tl_db.debug("insert_new_customer()")
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
                logger_tl_db.debug("Customer already in Database")
    except psycopg.Error as e:
        logger_tl_db.error(e)


def get_user_data(user_id: int, db_auth: dict) -> None:
    """Stuff"""
    logger_tl_db.info("get_user_data()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from users where user_id = %s", (user_id,))
        return result.fetchone()


def insert_user_phone_number(user_id: int, phone_number: int, db_auth: dict) -> None:
    logger_tl_db.debug("insert_customer_phone_number()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "update users set phone_number = %s where user_id = %s;",
            (phone_number, user_id),
        )
        conn.commit()
        logger_tl_db.info("Phone number added into Database")


def get_customer_data(user_id: int, db_auth: dict) -> List:
    logger_tl_db.debug("get_customer_data()")
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
    logger_tl_db.debug("get_customer_last_order_id()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where (customer_id = %s and contractor_id = %s)",
            (user_id, contractor_id),
        )
        orders = result.fetchall()
        logger_tl_db.debug(f"orders: {orders}")

        return orders[-1][0]


def insert_new_order(
    user_id: int, device_context: List, default_contractor_id: int, db_auth: dict
) -> None:
    logger_tl_db.debug("insert_new_order()")

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
    logger_tl_db.debug("get_order_data()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from orders where order_id = %s", (order_id,))

        return result.fetchone()


def get_open_orders(db_auth: dict) -> List[Tuple]:
    logger_tl_db.debug("get_open_orders()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where completed = 0 and contractor_id is null"
        )
        return result.fetchall()


def get_assigned_orders(db_auth: dict) -> List[Tuple]:
    logger_tl_db.debug("get_incomplete_orders()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from orders where completed = 0 and contractor_id is not null"
        )
        return result.fetchall()


def update_order_Complete(order_id: int, timestamp: str, db_auth: dict) -> None:
    logger_tl_db.debug("update_order_Complete()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "update orders set completed = %s, completed_date = %s where order_id = %s",
            (1, timestamp, order_id),
        )
        conn.commit()


def get_contractor_data(user_id: int, db_auth: dict) -> List:
    logger_tl_db.debug("get_contractor_data()")
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
    logger_tl_db.debug("get_all_contractor_ids()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select contractor_id from contractors")
        contractor_ids = [i[0] for i in result.fetchall()]

        return contractor_ids


def update_order_contractor_id(
    order_id: int, new_contractor_id: int, db_auth: dict
) -> None:
    logger_tl_db.debug("update_order_ContractID()")
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
    logger_tl_db.debug("insert_assign")
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
    logger_tl_db.debug("check_assign()")
    with create_db_connection(db_auth) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select * from assign where old_contractor_id = %s and order_id = %s and new_contractor_id = %s",
            (old_contractor_id, order_id, new_contractor_id),
        )

        return True if result.fetchone() else False


def insert_message(message_id: int, user_id: int, text: str, db_auth: dict) -> None:
    """Data collection"""
    logger_tl_db.debug("insert_message()")
    logger_tl_db.debug(f"inserting: {message_id}, {user_id}, {text}")

    with create_db_connection(db_auth) as conn:
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
            print(
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
                print(f"An error occurred during retry: {ex}")

        except Exception as ex:
            # Handle or log any other exception
            print(f"An unexpected error occurred: {ex}")
            conn.rollback()
