from typing import Optional, Dict, Any
from wallet.utils.db import db
from contextlib import contextmanager


class UserRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepo, cls).__new__(cls)
        return cls._instance

    @contextmanager
    def _get_cursor(self):
        """Helper method to get a cursor using the db singleton"""
        with db.get_cursor() as cursor:
            yield cursor

    def add_user(self, acc_num, name, tier):
        with self._get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (acc_num, name, type, balance) VALUES (%s, %s, %s, %s)",
                (acc_num, name, tier, 0.0)
            )
            return True

    def find_user(self, identifier, by_acc_num = True):
        with self._get_cursor() as cursor:
            query = ("SELECT id, acc_num, name, type, balance FROM users WHERE "
                     "acc_num = %s" if by_acc_num else "id = %s")
            cursor.execute(query, (identifier,))
            user = cursor.fetchone()

            if user:
                return {
                    "id": user[0],
                    "acc_num": user[1],
                    "name": user[2],
                    "type": user[3],
                    "balance": float(user[4])
                }
            return None

    def update_balance(self, user_id, amount, operation= 'add'):
        with self._get_cursor() as cursor:
            if operation == 'add':
                cursor.execute(
                    "UPDATE users SET balance = balance + %s WHERE id = %s RETURNING balance",
                    (amount, user_id)
                )
            elif operation == 'subtract':
                cursor.execute(
                    "UPDATE users SET balance = balance - %s WHERE id = %s RETURNING balance",
                    (amount, user_id)
                )
            else:
                raise ValueError("Invalid operation. Use 'add' or 'subtract'")

            result = cursor.fetchone()
            return float(result[0]) if result else None