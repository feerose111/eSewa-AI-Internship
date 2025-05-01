import db , psycopg2
class Transaction:
    def __init__(self, user_id, tx_type, amount, status = 'pending' , remarks = None):
        self.user_id = user_id
        self.tx_type = tx_type
        self.amount = amount
        self.status = status
        self.remarks = remarks

    def deposit(self):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (self.amount, self.user_id))
            self.record_transaction(receiver_id=self.user_id)
            conn.commit()
        except psycopg2.OperationalError as e:
            print("Deposit failed.", e)
        finally:
            cur.close()
            conn.close()

    def withdraw(self):
        try:
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
        except psycopg2.IntegrityError as e:
            print("Withdrawal failed due to integrity issue:", e)
            return False
        finally:
            cur.close()
            conn.close()

    def transfer(self, receiver_id):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT balance FROM users WHERE id = %s", (self.user_id,))
            current_balance = cur.fetchone()[0]
            if current_balance >= self.amount:
                cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (self.amount, self.user_id))
                cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (self.amount, receiver_id))
                conn.commit()
                self.record_transaction(sender_id=self.user_id, receiver_id=receiver_id)
                success = True
            else:
                print("Insufficient balance to transfer.")
                success = False
        except psycopg2.IntegrityError as e:
            print("Transfer failed due to integrity issue:", e)
            return False
        finally:
            cur.close()
            conn.close()

    def record_transaction(self, sender_id=None, receiver_id=None):
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO transactions (sender_id, receiver_id, type, status, remarks)
                VALUES (%s, %s, %s, %s)""", (sender_id, receiver_id, self.tx_type, 'completed', self.remarks))
            conn.commit()
        except psycopg2.DatabaseError as e:
            print("Transaction logging failed:", e)
        finally:
            cur.close()
            conn.close()


