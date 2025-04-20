from expenseTracker import Tracker


def main():

    while True:
        print('\n Add Total Monthly Budget')
        try:
            amount = int(input('Enter your monthly budget : '))
            tracker = Tracker()
            result = tracker.addBudget(amount)
            print('Your Monthly Budget is ', amount)
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
                            category = str(input(f'Enter Category from {Tracker.category}: ')).lower()
                            if category not in Tracker.category:
                                print('Please! Chose a category from the list')
                                print('If your category is not in the list you can create a new category !!')
                                if category == 'new category':
                                    newCat = str(input('Enter a new category to add :')).lower()
                                    tracker.addCategory(newCat)
                                    print("New Category added !")
                                else:
                                    continue
                            else:
                                break
                        expense = int(input('Add Expense : '))

                        result = tracker.budgetTracker(expense)
                        tracker.saveTransaction()
                        tracker.showHistory(f'Added {expense} to {category}')

                        tracker.budget = result['remaining budget']

                        print('Budget Updated')

                case 2:
                    remBalance = Tracker.transaction[-1]['remaining budget']
                    print('Your remaining balance is ', remBalance)
                    tracker.showHistory(f'Showed remaining budget : {remBalance}')


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