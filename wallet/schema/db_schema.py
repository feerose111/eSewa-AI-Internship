import psycopg2
from wallet.utils.config import DB_CONFIG

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
