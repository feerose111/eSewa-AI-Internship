from user import User
from transaction import Transaction
import db
import random


def main():
    print("Welcome to your personal wallet. ")
    name = input("Enter user name: ")
    tier = input("Enter tier (personal/premium/Business): ")

    db.add_user(name, tier)
    user = User(random.randint(1,100000), name, tier)

    amount = float(input("Enter amount to deposit: "))
    user.wallet.deposit(amount)
    db.log_transaction(user.user_id, "deposit", amount)

    print(f"{user.name} now has balance: Rs.{user.wallet.balance:.2f}")


if __name__ == "__main__":
    main()
