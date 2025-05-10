from transaction import Transaction
class User:
    def __init__(self, user_id, name, acc_num=None, tier="basic", balance= 0.0):
        self.user_id = user_id
        self.name = name
        self.acc_num = acc_num
        self.tier = tier
        self.balance = balance

    def show_menu(self):
        while True:
            print(f"\nWelcome, {self.name}!")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer")
            print("4. Show Balance")
            print("5. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                try:
                    amount = float(input("Enter amount to deposit: "))
                    if amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                    tx = Transaction(self.user_id, "deposit", amount = amount)
                    if tx.deposit():
                        self.balance = tx.get_balance()
                        print(f"Deposited Rs.{amount:.2f}. New balance: Rs.{self.balance:.2f}")
                    else:
                        print("Deposit failed.")
                except ValueError as e:
                    print(f'Invalid input : {e}')

            elif choice == "2":
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    if amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                    remarks = input("Enter remarks for withdrawal: ")
                    tx = Transaction(self.user_id, "withdraw", amount =amount , remarks = remarks)
                    if tx.withdraw():
                        self.balance = tx.get_balance()
                        print(f"Withdrawn Rs.{amount:.2f}. New balance: Rs.{self.balance:.2f}")
                    else:
                        print("Insufficient balance.")
                except ValueError as e:
                    print(f'Invalid input : {e}')

            elif choice == "3":
                try:
                    receiver_acc_num = int(input("Enter receiver's account number: "))
                    amount = float(input("Enter amount to transfer: "))
                    if amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                    remarks = input("Enter remarks for transfer: ")
                    tx = Transaction(self.user_id, "transfer", amount = amount, remarks=remarks)
                    if tx.transfer(receiver_acc_num):
                        self.balance = tx.get_balance()
                        #self.wallet -= amount
                        print(f"Transferred Rs.{amount:.2f} to user ID {receiver_acc_num}. New balance: Rs.{self.balance:.2f}")
                    else:
                        print("Transfer failed due to insufficient balance.")
                except ValueError as e:
                    print(f"Invalid input: {e}")
                except Exception as e:
                    print(f"Error processing transfer: {e}")

            elif choice == "4":
                print(f"Balance: Rs.{self.balance:.2f}")

            elif choice == "5":
                exit_choice = input("Do you want to exit from your profile? (y/n) ").lower()
                if exit_choice == "y":
                    break
                else:
                    continue

            else:
                print("Invalid choice. Try again.")