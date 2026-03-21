import unittest
from unittest.mock import patch

from database.connection import managed_connection


class FakeConnection:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class ManagedConnectionTests(unittest.TestCase):
    def test_managed_connection_commits_and_closes_on_success(self):
        fake_connection = FakeConnection()

        with patch("database.connection.get_connection", return_value=fake_connection):
            with managed_connection() as connection:
                self.assertIs(connection, fake_connection)

        self.assertTrue(fake_connection.committed)
        self.assertFalse(fake_connection.rolled_back)
        self.assertTrue(fake_connection.closed)

    def test_managed_connection_rolls_back_and_closes_on_error(self):
        fake_connection = FakeConnection()

        with patch("database.connection.get_connection", return_value=fake_connection):
            with self.assertRaises(RuntimeError):
                with managed_connection():
                    raise RuntimeError("forced failure")

        self.assertFalse(fake_connection.committed)
        self.assertTrue(fake_connection.rolled_back)
        self.assertTrue(fake_connection.closed)


if __name__ == "__main__":
    unittest.main()

