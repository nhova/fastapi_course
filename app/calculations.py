def add(num1: int, num2: int):
  return num1 + num2

def sub(num1: int, num2: int):
  return num1 - num2

def mult(num1: int, num2: int):
  return num1 * num2

def div(num1: int, num2: int):
  return num1 / num2

class InsufficientFunds(Exception):
  pass

class BankAccount():
  def __init__(self, starting_balance=0):
    self.balance = starting_balance

  def deposit(self, amount):
    self.balance += amount

  def withdraw(self, amount):
    if amount > self.balance:
      raise InsufficientFunds("Insufficient funds")
    self.balance -= amount

  def collect_interest(self):
    self.balance *= 1.1

my_account = BankAccount(100)
my_account.deposit(20)
my_account.withdraw(10)
my_account.collect_interest()

print(my_account.balance)