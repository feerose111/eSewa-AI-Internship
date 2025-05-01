from user import User
from transaction import Transaction
import db
import random


def main():
    print("Welcome to your personal wallet. ")
    while True:
        print("1. Sign In")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter your name: ")
            user_data = db.find_user(name)

            if user_data:
                print("\n Welcome back!")
                print(f"ID: {user_data['id']}")
                print(f"Name: {user_data['name']}")
                print(f"Tier: {user_data['type']}")
                print(f"Balance: Rs.{user_data['balance']:.2f}")
                user = User(
                    user_id = user_data["id"],
                    name = user_data["name"],
                    tier = user_data["type"],
                    balance = user_data["balance"]
                )
                user.show_menu()
            else:
                print("User not found. Please register first.")

        elif choice == "2":
            id = random.randint(1, 100000)
            name = input("Enter your name: ")
            tier = input("Enter tier (personal/premium/business): ").lower()

            if tier not in ("personal", "premium", "business"):
                print("Invalid tier. Defaulting to 'personal'.")
                tier = "personal"

            db.add_user(id, name, tier)
            print(f"\nAccount created for {name} with tier '{tier}'.")

            # Confirm by fetching user
            user_data = db.find_user(name)
            print(f"ID: {user_data['id']}")
            print(f"Balance: Rs.{user_data['balance']:.2f}")
            user = User(
                user_id = user_data["id"],
                name = user_data["name"],
                tier = user_data["type"],
                balance = user_data["balance"]
            )
            user.show_menu()

        elif choice == '3':
            exit = input('Do you want to exit the wallet?(y/n)').lower()
            if exit == 'y':
                print('Exiting the Wallet. GoodBye!')
                break
            else:
                continue
        else:
            print("Invalid option. Please run the program again.")

if __name__ == "__main__":
    main()
