from wallet.utils.db import db
from contextlib import contextmanager

class TransactionRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TransactionRepo, cls).__new__(cls)
        return cls._instance

    @contextmanager
    def _get_cursor(self):
        """Helper method to get a cursor using the db singleton"""
        with db.get_cursor() as cursor:
            yield cursor

    @contextmanager
    def _get_transaction_cursor(self):
        """Helper method for transactions needing explicit control"""
        with db.get_connection() as conn:
            conn.autocommit = False
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                cursor.close()

    def record_transaction(self, sender_id=None, receiver_id=None, tx_type="deposit",
                         amount=0.0, status="completed", remarks=None):
        with self._get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO transactions 
                (sender_id, receiver_id, type, amount, status, remarks)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (sender_id, receiver_id, tx_type, amount, status, remarks))
            return True

    def get_daily_total(self,user_id, tx_type):
            with self._get_cursor() as cursor:
                    cursor.execute("""
                        SELECT COALESCE(SUM(amount), 0) /* Handles NULL value by returning 0 */
                        FROM transactions 
                        WHERE sender_id = %s AND type = %s AND DATE(timestamp) = CURRENT_DATE AND status = 'completed'
                    """, (user_id, tx_type))
                    total = cursor.fetchone()[0]
                    return float(total)

    def transfer_funds(self, sender_id, receiver_id, amount, tx_type, remarks):
        try:
            with self._get_transaction_cursor() as cursor:
                cursor.execute(
                    "SELECT balance FROM users WHERE id = %s FOR UPDATE",
                    (sender_id,)
                )
                sender_balance = float(cursor.fetchone()[0])

                if sender_balance < amount:
                    return False

                #Deduct from sender
                cursor.execute(
                    "UPDATE users SET balance = balance - %s WHERE id = %s",
                    (amount, sender_id)
                )

                #Add to receiver
                cursor.execute(
                    "UPDATE users SET balance = balance + %s WHERE id = %s",
                    (amount, receiver_id)
                )

                #Record transaction
                cursor.execute("""
                    INSERT INTO transactions 
                    (sender_id, receiver_id, type, amount, status, remarks)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (sender_id, receiver_id, tx_type, amount, 'completed', remarks))

                return True

        except Exception as e:
            self.record_transaction(
                sender_id=sender_id,
                receiver_id=receiver_id,
                tx_type=tx_type,
                amount=amount,
                status='failed',
                remarks=f"Failed: {str(e)}"
            )
            return False