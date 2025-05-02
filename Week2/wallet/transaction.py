import db , psycopg2
class Transaction:
    def __init__(self, user_id, tx_type, amount, status = 'pending' , remarks = None):
        self.user_id = user_id #primary key
        self.tx_type = tx_type
        self.amount = amount
        self.status = status
        self.remarks = remarks
        self.current_balance = 0.0

    def get_balance(self):
        return self.current_balance

    def deposit(self):
        try:
            new_balance = db.update_balance(self.user_id, self.amount, 'add')
            if new_balance is not None:
                self.current_balance = new_balance
                db.record_transaction(receiver_id=self.user_id, tx_type=self.tx_type,
                                      amount=self.amount, status='completed', remarks=self.remarks)
                return True
            return False
        except Exception as e:
            print(f"Deposit failed: {e}")
            db.record_transaction(receiver_id=self.user_id, tx_type=self.tx_type,
                                  amount=self.amount, status='failed', remarks=self.remarks)
            return False

    def withdraw(self):
        try:
            # Get current balance
            current_balance = db.get_user_balance(self.user_id)

            if current_balance >= self.amount:
                # CHANGE: Store the new balance returned by update_balance
                new_balance = db.update_balance(self.user_id, self.amount, 'subtract')
                if new_balance is not None:
                    self.current_balance = new_balance
                    db.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                          amount=self.amount, status='completed', remarks=self.remarks)
                    return True
            else:
                print("Insufficient balance.")
                db.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                      amount=self.amount, status='failed', remarks=self.remarks)
                return False
        except Exception as e:
            print(f"Withdrawal failed: {e}")
            db.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                  amount=self.amount, status='failed', remarks=self.remarks)
            return False

    def transfer(self, receiver_acc_num):
        try:
            receiver_data = db.find_user(receiver_acc_num)
            if not receiver_data:
                print(f"Receiver account #{receiver_acc_num} not found.")
                return False

            receiver_id = receiver_data['id']
            current_balance = db.get_user_balance(self.user_id)

            if current_balance >= self.amount:
                with db.get_connection() as conn:
                    try:
                        conn.autocommit = False
                        with conn.cursor() as cur:
                            cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s RETURNING balance",
                                        (self.amount, self.user_id))
                            sender_balance = float(cur.fetchone()[0])

                            # Add to receiver
                            cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s",
                                        (self.amount, receiver_id))
                            cur.execute("""
                                INSERT INTO transactions (sender_id, receiver_id, type, amount, status, remarks)
                                VALUES (%s, %s, %s, %s, %s, %s)""",
                                        (self.user_id, receiver_id, self.tx_type, self.amount, 'completed',
                                         self.remarks))

                            conn.commit()
                            self.current_balance = sender_balance
                            return True
                    except Exception as e:
                        # Rollback on error
                        conn.rollback()
                        print(f"Transfer failed, rolling back transaction: {e}")
                        # Record failed transaction
                        db.record_transaction(sender_id=self.user_id, receiver_id=receiver_id,
                                              tx_type=self.tx_type, amount=self.amount,
                                              status='failed', remarks=self.remarks)
                        return False
            else:
                print("Insufficient balance to transfer.")
                if receiver_data:
                    db.record_transaction(sender_id=self.user_id, receiver_id=receiver_id,
                                          tx_type=self.tx_type, amount=self.amount,
                                          status='failed', remarks=self.remarks)
                return False
        except Exception as e:
            print(f"Transfer error: {e}")
            return False
