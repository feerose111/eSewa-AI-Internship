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
        self.cataName = None

    def addCategory(self, cataName):
        self.cataName = cataName
        if cataName not in Tracker.category:
            Tracker.category.append(cataName)

    def addBudget(self, budget):
        self.budget = budget
        return self.budget

    def budgetTracker(self, expense):
        self.expense = expense
        remBudget = self.budget
        id = random.randint(1,100000)
        date = datetime.datetime.now(tzNepal).strftime("%Y-%m-%d %X%p ")
        if self.expense > remBudget:
            print('Your expense exceeds your budget !!')
            return None
        elif self.expense > 0 :
            remBudget -= self.expense

        transaction_data = ({
                'id':id,
                'datetime': date,
                'total budget':self.budget,
                'category':self.cataName,
                'categories':Tracker.category,
                'remaining budget': remBudget})
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

    def savings(self):
        pass









