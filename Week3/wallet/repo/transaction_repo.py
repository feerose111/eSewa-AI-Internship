import Week3.wallet.utils.db as db
import psycopg2

class TransactionRepo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TransactionRepo, cls).__new__(cls)
            cls._instance.db = db
        return cls._instance

    def record_transaction(self, sender_id=None, receiver_id=None, tx_type="deposit", amount=0.0, status="completed", remarks=None):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO transactions (sender_id, receiver_id, type, amount, status, remarks)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (sender_id, receiver_id, tx_type, amount, status, remarks))
                    conn.commit()
                    return True
        except psycopg2.DatabaseError as e:
            print(f"Transaction logging failed: {e}")
            return False

    def get_daily_total(self,user_id, tx_type):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT COALESCE(SUM(amount), 0) /* Handles NULL value by returning 0 */
                        FROM transactions 
                        WHERE sender_id = %s AND type = %s AND DATE(timestamp) = CURRENT_DATE AND status = 'completed'
                    """, (user_id, tx_type))
                    total = cur.fetchone()[0]
                    return float(total)
        except Exception as e:
            print(f"Error calculating daily total: {e}")
            return 0.0