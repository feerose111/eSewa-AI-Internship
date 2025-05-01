from transaction import Transaction
class User:
    def __init__(self, user_id, name, tier="personal", balance= 0.0):
        self.user_id = user_id
        self.name = name
        self.tier = tier
        self.wallet = balance

    def show_menu(self):
        while True:
            print(f"\nWelcome, {self.name}!")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Show Balance")
            print("4. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                amount = float(input("Enter amount to deposit: "))
                tx = Transaction(self.user_id, "deposit", amount)
                tx.deposit()
                self.wallet += amount
                print(f"Deposited Rs.{amount:.2f}. New balance: Rs.{self.wallet:.2f}")

            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                tx = Transaction(self.user_id, "withdraw", amount)
                if tx.withdraw():
                    self.wallet -= amount
                    print(f"Withdrawn Rs.{amount:.2f}. New balance: Rs.{self.wallet:.2f}")
                else:
                    print("Insufficient balance.")

            elif choice == "3":
                print(f"Balance: Rs.{self.wallet:.2f}")

            elif choice == "4":
                exit = input("Do you want to exit from your profile? (y/n) ").lower()
                if exit == "y":
                    break
                else:
                    continue

            else:
                print("Invalid choice. Try again.")