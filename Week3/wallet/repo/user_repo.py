import Week3.wallet.utils.db as db
import psycopg2

class UserRepo:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserRepo, cls).__new__(cls)
            cls._instance.db = db
        return cls._instance

    def add_user(self, acc_num, name, tier):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO users (acc_num, name, type, balance) VALUES (%s, %s, %s, %s)", (acc_num, name, tier, 0.0))
                    conn.commit()
        except psycopg2.Error as e:
            print(f"Database error during user creation: {e}")

    def find_user(self, acc_num):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT id, acc_num, name, type, balance FROM users WHERE acc_num = %s", (acc_num,))
                    user = cur.fetchone()
                    if user:
                        return {
                            "id": user[0],
                            "acc_num": user[1],
                            "name": user[2],
                            "type": user[3],
                            "balance": float(user[4])
                        }
                    else:
                        return None
        except Exception as e:
            print("Error fetching user by account number:", e)
            return None

    def update_balance(self, user_db_id, amount, operation='add'):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    if operation == 'add':
                        cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s RETURNING balance",
                                    (amount, user_db_id))
                    elif operation == 'subtract':
                        cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s RETURNING balance",
                                    (amount, user_db_id))
                    result = cur.fetchone()
                    conn.commit()
                    if result:
                        return float(result[0])  # Return the new balance
                    return None
        except Exception as e:
            print(f"Error updating balance: {e}")
            return None

    def get_user_balance(self, user_db_id):
        try:
            with self.db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT balance FROM users WHERE id = %s", (user_db_id,))
                    result = cur.fetchone()
                    if result:
                        return float(result[0])
                    return 0.0
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0

    def get_user_tier(self, user_db_id):
            try:
                with self.db.get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT type FROM users WHERE id = %s", (user_db_id,))
                        result = cur.fetchone()
                        if result:
                            return result[0]
                        return None
            except Exception as e:
                print(f"Error getting tier info: {e}")
                return None
