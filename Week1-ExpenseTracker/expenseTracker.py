import json
import pandas as pd
import random
import datetime , pytz

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
            df = pd.DataFrame(Tracker.transaction)
            df.to_csv("transactions.csv", mode='w', index=False, header=True)
            print("Transaction Successful, Updated your budget !!")

    def showHistory(self):
        pass



