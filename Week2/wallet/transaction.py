import db , psycopg2
from utils import get_user_tier_info
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

    def is_allowed(self, tx_category):
        """checks the rules set for each tier of user"""
        tier_info, tier = get_user_tier_info(self.user_id)

        if self.amount > tier_info["max_per_transaction"]:
            print(f"{tx_category.capitalize()} limit exceeded. Max per transaction for {tier}: Rs.{tier_info['max_per_transaction']}")
            return False

        daily_total = db.get_daily_total(self.user_id, tx_category)
        if daily_total + self.amount > tier_info["max_daily_total"]:
            print(f"Daily {tx_category} limit exceeded. Max daily total: Rs.{tier_info['max_daily_total']}")
            return False

        return True

    def deposit(self):
        try:
            if not self.is_allowed("deposit"):
                return False

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
            if not self.is_allowed("withdraw"):
                return False
            current_balance = db.get_user_balance(self.user_id)

            if current_balance >= self.amount:
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

            #rules checking for each tier before transfer and transfer fee deduction
            if not self.is_allowed("transfer"):
                return False
            tier_info, _ = get_user_tier_info(self.user_id)
            fee = (tier_info["transfer_fee_percent"] / 100) * self.amount
            total_deduct = self.amount + fee

            current_balance = db.get_user_balance(self.user_id)

            if current_balance >= total_deduct:
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
