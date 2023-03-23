from configparser import ConfigParser
import logging
import sqlite3

from typing import List, Tuple

from resources.constants_loader import load_constants

constants = load_constants()
DB_FILEPATH = constants.get("FILEPATH", "SERVER_DATABASE")

logger_tl_db = logging.getLogger(__name__)


def insert_new_user(user_id: int, username: str, first_name: str, last_name: str) -> None:
    """Stuff"""
    logger_tl_db.debug("insert_new_customer()")
    try:
        with sqlite3.connect(DB_FILEPATH) as conn:
            cursor = conn.cursor()
            result = cursor.execute("select * from Users where UserID = ?", (user_id,))
            if result.fetchone() is None:
                cursor.execute("insert into Users (UserID, UserName, FirstName, LastName) values (?, ?, ?, ?);",
                               (user_id, username, first_name, last_name))
                conn.commit()
            else:
                logger_tl_db.debug("Customer already in Database")
    except sqlite3.Error as e:
        logger_tl_db.error(e)



def get_user_data(user_id: int) -> None:
    """Stuff"""
    logger_tl_db.info("get_user_data()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Users where UserID = ?", (user_id,))
        return result.fetchone()


def insert_user_phone_number(user_id: int, phone_number: int) -> None:
    logger_tl_db.debug("insert_customer_phone_number()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("update Users set PhoneNumber = ? where UserID = ?;", (phone_number, user_id))
        conn.commit()
        logger_tl_db.info("Phone number added into Database")


def get_customer_data(user_id: int) -> List:
    logger_tl_db.debug("get_customer_data()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select Users.UserID, Users.UserName, Users.FirstName, Users.LastName,"
                                "Users.PhoneNumber, Users.JoinDate, "
                                "Customers.Warning "
                                "from Users, Customers "
                                "where UserID = ?1 and CustomerID = ?1", (user_id,))

        return result.fetchone()


def get_customer_last_OrderID(user_id: int, contractor_id: int = None) -> int:
    logger_tl_db.debug("get_customer_last_OrderID()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Orders where (CustomerID = ? and ContractorID is ?)",
                                (user_id, contractor_id))
        orders = result.fetchall()
        logger_tl_db.info("orders: {}".format(orders))

        return orders[-1][0]


def insert_new_order(user_id: int, device_context: dict, default_contractor_id: int = None) -> None:
    logger_tl_db.debug("insert_new_order()")

    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("insert into Orders (CustomerID, ContractorID, OS, Device, Category, Problem) "
                           "values (?, ?, ?, ?, ?, ?);",
                           (user_id, default_contractor_id,
                            device_context["OS"], device_context["Device"],
                            device_context["Category"], device_context["Problem"]))
        except TypeError:
            logger_tl_db.info("device_context == NoneType")
            cursor.execute("insert into Orders (CustomerID, ContractorID, OS, Device, Category, Problem) "
                           "values (?, ?, ?, ?, ?, ?);", (user_id, default_contractor_id, None, None, None, None))
        conn.commit()


def get_order_data(OrderID: int) -> List:
    logger_tl_db.debug("get_order_data()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Orders where OrderID = ?", (OrderID,))

        return result.fetchone()


def get_open_orders() -> List[Tuple]:
    logger_tl_db.debug("get_open_orders()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Orders where Completed = 0 and ContractorID is null")
        return result.fetchall()


def get_assigned_orders() -> List[Tuple]:
    logger_tl_db.debug("get_incomplete_orders()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Orders where Completed = 0 and ContractorID is not null")
        return result.fetchall()


def update_order_Complete(OrderID: int, timestamp: str) -> None:
    logger_tl_db.debug("update_order_Complete()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("update Orders set Completed = ?, CompletedDate = ? where OrderID = ?",
                       (1, timestamp, OrderID))
        conn.commit()


def get_contractor_data(user_id: int) -> List:
    logger_tl_db.debug("get_contractor_data()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute(
            "select Users.UserID, Users.UserName, Users.FirstName, Users.LastName, Users.PhoneNumber, Users.JoinDate, "
            "Contractors.Warning "
            "from Users, Contractors "
            "where UserID = ?1 and ContractorID = ?1", (user_id,))

        return result.fetchone()


def get_all_ContractorID() -> List:
    logger_tl_db.debug("get_all_contractor_ids()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select ContractorID from Contractors")
        ContractorIDs = [i[0] for i in result.fetchall()]

        return ContractorIDs


def update_order_ContractorID(OrderID: int, new_ContractorID: int) -> None:
    logger_tl_db.debug("update_order_ContractID()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("update Orders set ContractorID = ? where OrderID = ?",
                       (new_ContractorID, OrderID))
        conn.commit()


def insert_assign(old_ContractorID: int, OrderID: int, new_ContractorID: int) -> None:
    logger_tl_db.debug("insert_assign")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("insert into Assign (old_ContractorID, OrderID, new_ContractorID) "
                       "values (?, ?, ?);",
                       (old_ContractorID, OrderID, new_ContractorID))
        conn.commit()


def check_assign(old_ContractorID: int, OrderID: int, new_ContractorID: int) -> bool:
    logger_tl_db.debug("check_assign()")
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        result = cursor.execute("select * from Assign where old_ContractorID = ? and OrderID = ? and new_ContractorID = ?",
                                (old_ContractorID, OrderID, new_ContractorID))

        return True if result.fetchone() else False


def insert_message(MessageID: int, UserID: int, text: str) -> None:
    """Data collection"""
    logger_tl_db.debug("insert_message()")
    logger_tl_db.debug("inserting: {}, {}, {}".format(MessageID, UserID, text))
    with sqlite3.connect(DB_FILEPATH) as conn:
        cursor = conn.cursor()
        cursor.execute("insert into Messages (MessageID, UserID, MessageText) values (?, ?, ?)",
                       (MessageID, UserID, text))
        conn.commit()


if __name__ == "__main__":
    print(DB_FILEPATH)
