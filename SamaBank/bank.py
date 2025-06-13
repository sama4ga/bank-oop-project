from user import User
from account import Account, AccountType, AccountStatus
from nimc import NIMC


class Bank():
  def __init__(self, name, start_index, nimc:NIMC):
    self._start_index = start_index
    self.name = name
    self._accounts = {}
    self._nimc = nimc

  def __str__(self):
    return self.name

  def create_account(self, nin:int) -> Account:
    user = self._nimc.get_user(nin)
    if user is None:
      raise ValueError("Invalid NIN supplied")
    
    account = Account(user, self._start_index)
    self._accounts[user] = account
    self._start_index += 1
    return account

  def get_account(self, account_no) -> Account|None:
    acc = None
    for account in self._accounts.values():
      if account.account_no == account_no:
        acc = account
        break
    return acc
  
  def get_user(self, account_no) -> User|None:
    for user, account in self._accounts.items():
      if account.account_no == account_no:
        return user
    return None

if __name__ == "__main__":
  from nimc import NIMC

  # create users for NIMC portal 
  nimc  = NIMC()
  maurice = nimc.register_user("Maurice")
  maurice_nin = maurice.nin
  peace = nimc.register_user("Peace")
  peace_nin = peace.nin
  tony = nimc.register_user("Anthony")
  tony_nin = tony.nin

  # create Bank and accounts
  sama_bank = Bank("SamaBank", 1, nimc)
  maurice_account = sama_bank.create_account(maurice_nin)
  peace_account = sama_bank.create_account(peace_nin)

  # transact with the accounts in the bank
  m_acc = sama_bank.get_account(maurice_account.account_no)
  p_acc = sama_bank.get_account(peace_account.account_no)
  m_acc.deposit(5000)
  m_acc.withdraw(1000)
  m_acc.transfer(p_acc, 3000)

  # inter-bank transfer
  otu_bank = Bank("Otu Bank", 10000, nimc)
  tony_account = otu_bank.create_account(tony_nin)
  t_acc = otu_bank.get_account(tony_account.account_no)
  p_acc.transfer(t_acc, 1000)

  print(m_acc)
  print(p_acc)
  print(t_acc)