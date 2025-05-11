from wallet.repo.transaction_repo import TransactionRepo
from wallet.repo.user_repo import UserRepo
from wallet.utils.utils import get_user_tier_info
from wallet.model.transaction_model import TransactionModel

class TransactionService:

    def __init__(self,data : TransactionModel):
        self.user_id = data.id #primary key
        self.tx_type = data.tx_type
        self.amount = data.amount
        self.status = data.status
        self.remarks = data.remarks
        self.current_balance = 0.0

        self.wallet = TransactionRepo()
        self.user = UserRepo()

    def get_balance(self):
        return self.current_balance

    def is_allowed(self, tx_category):
        """checks the rules set for each tier of user"""
        tier_info, tier = get_user_tier_info(self.user, self.user_id)

        if self.amount > tier_info["max_per_transaction"]:
            print(f"{tx_category.capitalize()} limit exceeded. Max per transaction for {tier}: Rs.{tier_info['max_per_transaction']}")
            return False

        daily_total = self.wallet.get_daily_total(self.user_id, tx_category)
        if daily_total + self.amount > tier_info["max_daily_total"]:
            print(f"Daily {tx_category} limit exceeded. Max daily total: Rs.{tier_info['max_daily_total']}")
            return False

        return True

    def deposit(self):
        try:
            if not self.is_allowed("deposit"):
                return False

            new_balance = self.user.update_balance(self.user_id, self.amount, 'add')
            if new_balance is not None:
                self.current_balance = new_balance
                self.wallet.record_transaction(receiver_id=self.user_id, tx_type=self.tx_type,
                                      amount=self.amount, status='completed', remarks=self.remarks)
                return True
            return False
        except Exception as e:
            print(f"Deposit failed: {e}")
            self.wallet.record_transaction(receiver_id=self.user_id, tx_type=self.tx_type,
                                  amount=self.amount, status='failed', remarks=self.remarks)
            return False

    def withdraw(self):
        try:
            if not self.is_allowed("withdraw"):
                return False
            current_balance = self.user.get_user_balance(self.user_id)

            if current_balance >= self.amount:
                new_balance = self.user.update_balance(self.user_id, self.amount, 'subtract')
                if new_balance is not None:
                    self.current_balance = new_balance
                    self.wallet.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                          amount=self.amount, status='completed', remarks=self.remarks)
                    return True
            else:
                print("Insufficient balance.")
                self.wallet.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                      amount=self.amount, status='failed', remarks=self.remarks)
                return False
        except Exception as e:
            print(f"Withdrawal failed: {e}")
            self.wallet.record_transaction(sender_id=self.user_id, tx_type=self.tx_type,
                                  amount=self.amount, status='failed', remarks=self.remarks)
            return False

    def transfer(self, receiver_acc_num):
        """Handle the transfer business logic"""
        # 1. Find receiver
        receiver_data = self.user.find_user(receiver_acc_num)
        if not receiver_data:
            print(f"Receiver account #{receiver_acc_num} not found.")
            return False

        # 2. Check business rules
        if not self.is_allowed("transfer"):
            return False

        # 3. Calculate fee and total
        tier_info, _ = get_user_tier_info(self.user, self.user_id)
        fee = (tier_info["transfer_fee_percent"] / 100) * self.amount
        total_deduct = self.amount + fee

        # 4. Check balance
        current_balance = self.user.get_user_balance(self.user_id)
        if current_balance < total_deduct:
            print("Insufficient balance to transfer.")
            self.wallet.record_transaction(
                sender_id=self.user_id,
                receiver_id=receiver_data['id'],
                tx_type=self.tx_type,
                amount=self.amount,
                status='failed',
                remarks="Insufficient balance"
            )
            return False

        # 5. Perform transfer
        success = self.wallet.transfer_funds(
            sender_id=self.user_id,
            receiver_id=receiver_data['id'],
            amount=self.amount,
            tx_type=self.tx_type,
            remarks=self.remarks
        )

        if success:
            self.current_balance = current_balance - total_deduct
        return success
