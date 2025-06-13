from user import User
from enum import Enum

class AccountType(Enum):
  SAVING = 1
  CURRENT = 2

class AccountStatus(Enum):
  ACTIVE = 1
  FROZEN = 2
  BLOCKED = 3
  DORMANT = 4

class Account():
  ''' Account class for Banks '''
    
  def __init__(self, user:User, account_no:int):
    self._account_no = account_no
    self._balance = 0.0
    self._user = user
    # self.type = type
    # self.status = AccountStatus.ACTIVE

  def __hash__(self) -> int:
    return hash((self._account_no,))
  
  def __eq__(self, __value: object) -> bool:
    return (isinstance(__value, type(self)) and (self._account_no,) == (__value._account_no,))

  def __str__(self):
    return f"User: {self._user}\tAccount No.: {self.getAccountNo()}\tBalance: {self.getBalance()}"

  @property
  def account_no(self) -> int:
    return self._account_no
  
  @account_no.setter
  def account_no(self, value:int):
    raise NotImplementedError("Cannot modify account number")
    # if not isinstance(value, int):
    #   raise ValueError("Invalid account number supplied")
    # self._account_no = value

  @property
  def user(self):
    return self._user

  @user.setter
  def user(self, value:User):
    raise NotImplementedError("Cannot modify account user")
    # if not isinstance(value, User):
    #   raise ValueError("Invalid user supplied")
    # self._user = value

  @property
  def balance(self) -> float:
    return self._balance
  
  def getBalance(self) -> str:
    return f"{self._balance:0.2f} NGN"
  
  def getAccountNo(self) -> str:
    return str(self._account_no).zfill(10)

  def deposit(self, value:int|float):
    if not isinstance(value, (int,float)):
      raise ValueError("Invalid deposit amount")
    
    if value <= 0:
      raise ValueError("Deposit amount less than or equal to zero")

    self._balance += value

  def withdraw(self, value:int|float):
    ''' Withdrawal method. Overdraft not allowed '''

    if not isinstance(value, (int, float)):
      raise ValueError("Invalid withdrawal amount")
    
    if value <= 0:
      raise ValueError("Withdrawal amount less than or equal to zero")

    if self._balance <  value:
      raise ValueError("Insufficient amount")

    self._balance -= value

  def transfer(self, to, amount:int|float):
    if not isinstance(to, Account):
      raise ValueError("Invalid account supplied")
    self.withdraw(amount)
    to.deposit(amount)
