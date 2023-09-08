import unittest
from unittest.mock import Mock, patch

from src.common.database import utils


class TestDatabaseFunctions(unittest.TestCase):
    @patch("db_utils.create_db_connection")
    def test_insert_new_user(self, mock_create_db_connection):
        # Mock the connection and cursor
        mock_conn = Mock()
        mock_cursor = Mock()

        # Set the return_value of the connection's cursor() method
        mock_conn.cursor.return_value = mock_cursor

        # Set the return_value of the cursor's fetchone() method
        mock_cursor.fetchone.return_value = None

        # Set the return value of create_db_connection() to the mock connection
        mock_create_db_connection.return_value = mock_conn

        # Call the function you're testing
        db_utils.insert_new_user(123, "username", "first", "last")

        # Check that the execute() method was called with the right arguments
        mock_cursor.execute.assert_any_call(
            "select * from users where user_id = %s", (123,)
        )
        mock_cursor.execute.assert_any_call(
            "insert into users (user_id, user_name, first_name, last_name) values (%s, %s, %s, %s);",
            (123, "username", "first", "last"),
        )

        # Check that commit() was called on the connection
        mock_conn.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
