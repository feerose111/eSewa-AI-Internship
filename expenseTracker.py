import json
import pandas as pd
class Tracker:
    category = ['Food', 'other']
    transaction = []
    def __init__(self,budget,expense =0, cataName=None ):
        self.budget = budget
        self.expense = expense
        self.cataName = cataName

    def addCategory(self, cataName):
        self.cataName = cataName
        if cataName not in Tracker.category:
            Tracker.category.append(cataName)

    def budgetTracker(self, amount=0):
        self.budget += amount
        remBudget = self.budget
        if self.expense > self.budget:
            print('Your expense exceeds your budget !!')
        elif self.expense > 0 :
            remBudget -= self.expense

        transaction_data = ({
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



