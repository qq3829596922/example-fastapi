def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return a*b

def div(a,b):
    return a/b

class BankAccount:
    def __init__(self,balance=0):
        self.balance = balance

    def deposit(self,amount):
        self.balance += amount
    
    def withdraw(self,amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    
    def collect_interest(self):
        self.balance *= 1.1

    def get_balance(self):
        return round(self.balance,2)
        

