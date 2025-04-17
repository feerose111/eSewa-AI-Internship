from expenseTracker import Tracker
import json

def main():

    print('\n Add Total Monthly Budget')
    amount = int(input('Enter your monthly budget : '))
    tracker = Tracker(amount)
    result = tracker.budgetTracker()
    print( Tracker.transaction)
    print('Your Monthly Budget is ', result['total budget'])
    rembudget = Tracker.transaction[-1]['remaining budget']

    print('-------Expense Tracker--------')
    print('\n1. Add Expense')
    print('2. Show Remaining Budget')
    print('3. Show History')
    option = int(input('Please choose one of the options :'))
    try:
        match option:
            case 1:
                result = tracker.budgetTracker()
                category = str(input(f'Enter Category from {Tracker.category}: '))
                expense = int(input('Add Expense : '))
                t2 = Tracker(rembudget, expense, category )
                tracker.budgetTracker()


            case 2:
                pass


    except ValueError:
        print("Please enter a valid number")
    t = Tracker("Food", 500)
    print(Tracker.category)

    t.addCategory("Transport")
    print(Tracker.category)

    result = t.budgetTracker(10000)
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()