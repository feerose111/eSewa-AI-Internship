class Wallet:
    def __init__(self, balance=0.0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

class User:
    def __init__(self, user_id, name, tier="personal"):
        self.user_id = user_id
        self.name = name
        self.tier = tier
        self.wallet = Wallet()