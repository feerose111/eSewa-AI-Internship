import pandas as pd
import random
import datetime , pytz , os

tzNepal = pytz.timezone('Asia/Kathmandu')
class Tracker:
    category = ['food', 'other']
    transaction = []

    def __init__(self):
        self.budget = 0
        self.expense = 0
        self.saving = 0
        self.cataName = None

    def addCategory(self, cataName):
        self.cataName = cataName
        if cataName not in Tracker.category:
            Tracker.category.append(cataName)

    def addBudget(self, budget):
        self.budget = budget
        return self.budget

    def addSaving(self, percent):
        self.saving = (percent / 100) * self.budget
        self.budget -= self.saving
        self.showHistory(f'Saved {self.saving} ({percent}%) from total budget')
        print(f'Successfully set aside {self.saving} for savings.')
        return self.saving

    def budgetTracker(self, expense):
        self.expense = expense
        remBudget = self.budget
        id = random.randint(1,100000)
        date = datetime.datetime.now(tzNepal).strftime("%Y-%m-%d %X%p ")
        if self.expense > remBudget:
            lackingBudget = self.expense - remBudget
            print(f'Your expense amount exceeds your budget by: {lackingBudget}!!')
            if self.saving >= lackingBudget:
                choice = input("Do you want to use saving to cover this? (y/n): ").strip().lower()
                if choice == 'y':
                    self.saving -= lackingBudget
                    remBudget += lackingBudget
                    self.showHistory(f'Used {lackingBudget} from savings')
                    print(f'{lackingBudget} deducted from savings. Remaining saving: {self.saving}')
                else:
                    print("Returning to main menu without adding expense.")
                    self.showHistory('Chose not to use savings.')
                    return None
            else :
                print("Insufficient funds in both budget and savings to cover this expense.")
                return None
        remBudget -= self.expense

        if remBudget == 0:
            print("ALERT: Your budget is now completely depleted!")
            self.showHistory('Budget depleted to zero')

        elif remBudget < 100 :
            print('Your remaining balance is less than 100 !')
            save = input('Do you want to add the rest to saving? (y/n)').strip().lower()
            if save == 'y':
                self.saving += remBudget
                remBudget = 0
                print('Added remaining budget to saving.')
                self.showHistory(f'Remaining {remBudget} is added to savings')

        self.budget = remBudget

        transaction_data = ({
                'id':id,
                'datetime': date,
                'total budget':self.budget + self.expense,
                'category':self.cataName,
                'categories':Tracker.category,
                'remaining budget': remBudget,
                'saving' : self.saving,
        })
        Tracker.transaction.append(transaction_data)
        return transaction_data

    def saveTransaction(self):
        if not Tracker.transaction:
            print('No Transaction')
            return
        else:
            filename = 'transactions.csv'
            df = pd.DataFrame([Tracker.transaction[-1]])
            if os.path.exists(filename):
                df.to_csv(filename, mode='a', index=False, header=False)  # No header if file exists
            else:
                df.to_csv(filename, mode='w', index=False, header=True)
            print("Transaction Successful, Updated your budget !!")

    def showHistory(self, action):
        timestamp = datetime.datetime.now(tzNepal).strftime("%Y-%m-%d %X%p ")
        new_data = f'[{timestamp}],{action}\n'
        try:
            with open('history.txt', 'a') as file:
                file.write(new_data)

        except Exception as e:
            print("Error saving history:", e)









