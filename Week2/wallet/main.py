from user import User
import db
import random

def main():
    print("Welcome to your personal wallet. ")
    while True:
        print("1. Sign In")
        print("2. Register")
        print("3. Exit")

        choice = input("Choose an option: ")

        try:
            if choice == "1":

                num = int(input("Enter your account number: "))
                user_data = db.find_user(num)

                if user_data:
                    print("\nWelcome back!")
                    print(f"Account number: {user_data['acc_num']}")
                    print(f"Name: {user_data['name']}")
                    print(f"Tier: {user_data['type']}")
                    print(f"Balance: Rs.{user_data['balance']:.2f}")
                    user = User(
                        user_id = user_data["id"],
                        acc_num = user_data["acc_num"],
                        name = user_data["name"],
                        tier = user_data["type"],
                        balance = user_data["balance"]
                    )
                    user.show_menu()
                else:
                    print("User not found. Please register first.")

            elif choice == "2":
                acc_num = random.randint(1, 100000)
                name = input("Enter your name: ")
                tier = input("Enter tier (basic/premium/business): ").lower()

                if tier not in ("basic", "premium", "business"):
                    print("Invalid tier. Defaulting to 'personal'.")
                    tier = "basic"
                try:
                    db.add_user(acc_num, name, tier)

                    # Confirm by fetching user
                    user_data = db.find_user(acc_num)
                    if not user_data:
                        print("User creation failed. Please try again.")
                        continue
                    print(f"\nAccount created for {name} with tier '{tier}'.")
                    print(f"Account Number: {user_data['acc_num']}")
                    print(f"Balance: Rs.{user_data['balance']:.2f}")
                    user = User(
                        user_id = user_data["id"],
                        acc_num = user_data["acc_num"],
                        name = user_data["name"],
                        tier = user_data["type"],
                        balance = user_data["balance"]
                    )
                    user.show_menu()
                except Exception as e:
                    print(f"Error while creating user: {e}")

            elif choice == '3':
                exit = input('Do you want to exit the wallet?(y/n)').lower()
                if exit == 'y':
                    print('Exiting the Wallet. GoodBye!')
                    break
                else:
                    continue
            else:
                print("Invalid option. Please run the program again.")
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

if __name__ == "__main__":
    main()
