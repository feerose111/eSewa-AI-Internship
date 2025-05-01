import db
class Transaction:
    def __init__(self, user_id, tx_type, amount, status = 'pending'):
        self.user_id = user_id
        self.tx_type = tx_type
        self.amount = amount
        self.status = status

    def deposit(self):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (self.amount, self.user_id))
        self.record_transaction(receiver_id=self.user_id)
        conn.commit()
        cur.close()
        conn.close()

    def withdraw(self):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT balance FROM users WHERE id = %s", (self.user_id,))
        current_balance = cur.fetchone()[0]

        if current_balance >= self.amount:
            cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (self.amount, self.user_id))
            conn.commit()
            success = True
            self.record_transaction(sender_id=self.user_id)
        else:
            print("Insufficient balance in DB.")
            success = False

        cur.close()
        conn.close()
        return success

    def record_transaction(self, sender_id=None, receiver_id=None):
        conn = db.get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transactions (sender_id, receiver_id, type, status)
            VALUES (%s, %s, %s, %s)""", (sender_id, receiver_id, self.tx_type, 'completed'))
        conn.commit()
        cur.close()
        conn.close()


