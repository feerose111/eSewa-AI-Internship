import psycopg2
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Create users table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        acc_num INTEGER UNIQUE NOT NULL,
                        name TEXT NOT NULL,
                        type TEXT CHECK (type IN ('basic', 'premium', 'business')) NOT NULL DEFAULT 'basic',
                        balance NUMERIC(12, 2) DEFAULT 0.00
                    );
                """)

                # Create transactions table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        sender_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                        receiver_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                        datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        type TEXT CHECK (type IN ('deposit', 'withdraw', 'transfer')) NOT NULL,
                        amount NUMERIC(12, 2) NOT NULL,
                        status TEXT CHECK (status IN ('pending', 'failed', 'completed')) DEFAULT 'pending',
                        remarks TEXT
                    );
                """)

                conn.commit()
                print("Tables created successfully.")

    except Exception as e:
        print("Error creating tables:", e)


def add_user(acc_num, name, tier):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (acc_num, name, type, balance) VALUES (%s, %s, %s, %s)", (acc_num, name, tier, 0.0))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Database error during user creation: {e}")

def find_user(acc_num):
    try:
        with get_connection() as conn:
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

def update_balance(user_db_id, amount, operation='add'):
    try:
        with get_connection() as conn:
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

def get_user_balance(user_db_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT balance FROM users WHERE id = %s", (user_db_id,))
                result = cur.fetchone()
                if result:
                    return float(result[0])
                return 0.0
    except Exception as e:
        print(f"Error getting balance: {e}")
        return 0.0

def record_transaction(sender_id=None, receiver_id=None, tx_type="deposit", amount=0.0, status="completed", remarks=None):
    """Log a transaction in the database"""
    try:
        with get_connection() as conn:
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

if __name__ == "__main__":
    create_tables()