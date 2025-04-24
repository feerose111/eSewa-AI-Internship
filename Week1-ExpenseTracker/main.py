from expenseTracker import Tracker


def main():

    while True:
        print('\n Add Total Budget')
        try:
            amount = int(input('Enter your budget : '))
            tracker = Tracker()
            result = tracker.addBudget(amount)
            print('Your Budget is ', amount)
            tracker.showHistory(f'Set total budget: {amount}')
            break
        except ValueError:
            print("Invalid input! Please enter a valid number.")


    while True:
        print('-------Expense Tracker--------')
        print('\n1. Add Expense')
        print('2. Show Remaining Budget')
        print('3. Show History')
        print('4. Exit')
        option = int(input('Please choose one of the options :'))
        try:
            match option:
                case 1:
                        while True:
                            print(f'Available Categories : {Tracker.category}')
                            category = str(input(f"Enter Category (or type 'new' to add one) :  ")).lower()
                            if category == 'new':
                                newCat = str(input('Enter a new category to add :')).lower()
                                tracker.addCategory(newCat)
                                category = newCat
                                print("New Category added !")
                                continue
                            elif category not in Tracker.category:
                                continue
                            else:
                                break
                        tracker.cataName = category
                        expense = int(input('Add Expense : '))
                        result = tracker.budgetTracker(expense)
                        if result is None:
                            print('Insufficient Balance; You exited without making transaction!')
                            break
                        else:
                            tracker.saveTransaction()
                            tracker.showHistory(f'Added {expense} to {category}')
                            tracker.rembudget = result['remaining budget']

                case 2:
                    remBalance = Tracker.transaction[-1]['remaining budget']
                    print('Your remaining balance is ', remBalance)
                    tracker.showHistory(f'Showed remaining budget : {remBalance}')
                    percentage = (remBalance / amount) * 100
                    if percentage < 25:
                        print('Your Budget is getting low. Please spend wisely')

                case 3:
                    try:
                        with open("history.txt", "r") as file:
                            history = file.readlines()
                            if history:
                                latest_history = history[-5:][::-1]  # Get last 5 lines and reverse to show newest first
                                for idx, line in enumerate(latest_history, 1):
                                    print(f"{idx}. {line.strip()}")
                            else:
                                print("No history found yet.")
                    except FileNotFoundError:
                        print("No history file found yet.")

                case 4:
                    print('Exiting the expense tracker. GoodBye!')
                    tracker.showHistory('Exited expense tracker')
                    break

                case _:
                    print('Invalid option number!!')
                    tracker.showHistory('Chose invalid option')

        except ValueError:
            print("Please enter a valid number")
if __name__ == "__main__":
    main()