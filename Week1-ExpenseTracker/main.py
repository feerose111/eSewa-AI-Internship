from expenseTracker import Tracker


def main():

    print('\n Add Total Monthly Budget')
    amount = int(input('Enter your monthly budget : '))
    tracker = Tracker()
    result = tracker.addBudget(amount)
    print('Your Monthly Budget is ', amount ,'''result['total budget']''')


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
                    category = str(input(f'Enter Category from {Tracker.category}: ')).lower()
                    if category == 'other':
                        newCat = str(input('Enter a new category to add :')).lower()
                        tracker.addCategory(newCat)
                        print("New Category added !")
                        category = str(input(f'Enter Category from {Tracker.category}: ')).lower()
                    expense = int(input('Add Expense : '))

                    result = tracker.budgetTracker(expense)
                    tracker.saveTransaction()

                    tracker.budget = result['remaining budget']

                    print('Budget Updated')

                case 2:
                    remBalance = Tracker.transaction[-1]['remaining budget']
                    print('Your remaining balance is ', remBalance)

                case 3:
                    pass

                case 4:
                    print('Exiting the expense tracker. GoodBye!')
                    break

                case _:
                    print('Invalid option number!!')

        except ValueError:
            print("Please enter a valid number")
if __name__ == "__main__":
    main()