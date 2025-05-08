import pytest

from app.calculations import add,sub,mul,div,BankAccount


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account_50_dollars(zero_bank_account):
    return BankAccount(50)

@pytest.mark.parametrize("a,b,expected",[
    (1,2,3),
    (2,3,5),
    (3,4,7),
    (4,5,9),
    (5,6,11),
])
def test_add(a,b,expected):
    assert add(a,b) == expected

def test_sub():
    assert sub(1,2) == -1

def test_mul():
    assert mul(1,2) == 2

def test_div():
    assert div(1,2) == 0.5

def test_bank_account_default_amount():
    account = BankAccount()
    assert account.balance == 0

def test_bank_account_50_dollars(bank_account_50_dollars):
    assert bank_account_50_dollars.balance == 50

def test_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_account_withdraw(bank_account_50_dollars):
    bank_account_50_dollars.withdraw(20)
    assert bank_account_50_dollars.balance == 30

def test_bank_account_withdraw_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(200)

def test_bank_account_collect_interest(bank_account_50_dollars):
    bank_account_50_dollars.collect_interest()
    assert round(bank_account_50_dollars.balance,6) == 55

@pytest.mark.parametrize("deposited,withdrawn,expected",[
    (200,100,100),
    (50,10,40),
    (1200,200,1000),
    # (10,50,-40)
])
def test_bank_transaction(zero_bank_account,deposited,withdrawn,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(zero_bank_account):
    with pytest.raises(ValueError):
        zero_bank_account.withdraw(200)


