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
                        name TEXT NOT NULL,
                        type TEXT CHECK (type IN ('personal', 'premium', 'business')) NOT NULL DEFAULT 'personal',
                        balance NUMERIC(12, 2) DEFAULT 0.00,
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
                        status TEXT CHECK (status IN ('pending', 'failed', 'completed')) DEFAULT 'pending',
                        remarks TEXT
                    );
                """)

                conn.commit()
                print("Tables created successfully.")

    except Exception as e:
        print("Error creating tables:", e)

def find_user(name):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, type, balance FROM users WHERE name = %s", (name,))
                user = cur.fetchone()
                if user:
                    return {
                        "id": user[0],
                        "name": user[1],
                        "type": user[2],
                        "balance": float(user[3])
                    }
                else:
                    return None
    except Exception as e:
        print("Error fetching user:", e)
        return None

def add_user(id, name, tier):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (id, name, type, balance) VALUES (%s, %s, %s, %s)", (id, name, tier, 0.0))
            conn.commit()

def log_transaction(user_id, tx_type, amount):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO transactions (user_id, tx_type, amount) VALUES (%s, %s, %s)", (user_id, tx_type, amount))
            conn.commit()

if __name__ == "__main__":
    create_tables()