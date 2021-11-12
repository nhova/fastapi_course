import pytest
from app.calculations import *

@pytest.mark.parametrize("x, y, res", [(3, 2, 5), (5, 2, 7), (5, 3, 8), (6, 9, 15)])
def test_add(x, y, res):
  assert add (x, y)  == res

@pytest.mark.parametrize("x, y, res", [(3, 2, 1), (5, 2, 3), (5, 3, 2), (6, 9, -3)])
def test_sub(x, y, res):
  assert sub (x, y)  == res

@pytest.mark.parametrize("x, y, res", [(3, 2, 6), (5, 2, 10), (5, 3, 15), (6, 9, 54)])
def test_mult(x, y, res):
  assert mult (x, y)  == res

@pytest.mark.parametrize("x, y, res", [(4, 2, 2), (6, 2, 3), (9, 3, 3), (90, 9, 10)])
def test_div(x, y, res):
  assert div (x, y)  == res

@pytest.fixture
def zero_account():
  return BankAccount()

@pytest.fixture
def account():
  return BankAccount(50)

def test_bank_default_amount(zero_account):
  assert zero_account.balance == 0

def test_bank_set_amount(account):
  assert account.balance == 50

def test_withdraw(account):
  account.withdraw(20)
  assert account.balance == 30

def test_deposit(account):
  account.deposit(30)
  assert account.balance == 80

def test_interest(account):
  account.collect_interest()
  assert round(account.balance, 6) == 55

@pytest.mark.parametrize("d, w, r", [(40, 20, 20), (600, 50, 550), (500,500,0)])
def test_transaction(zero_account, d, w, r):
  zero_account.deposit(d)
  zero_account.withdraw(w)
  assert zero_account.balance == r

def test_insufficient_funds(account):
  with pytest.raises(InsufficientFunds):
    account.withdraw(200)