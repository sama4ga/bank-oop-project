from unittest import TestCase
from user import User
from nimc import NIMC
from bank import Bank
from account import Account

class UserTest(TestCase):
  def test_nin_not_editable_after_initialization(self):
    user = User("Test", 12345678)
    with self.assertRaises(AttributeError):
      user.nin = 987654321

  def test_nin_property_returns_nin(self):
    user = User("Test", 12345678)
    self.assertEqual(user.nin, 12345678)


class NIMCTest(TestCase):
  def setUp(self) -> None:
    self.nimc = NIMC()

  def test_register_user_returns_user(self):
    user = self.nimc.register_user("Test")
    self.assertIsInstance(user, User)
    self.assertEqual(user.nin, 1)

  def test_get_user_returns_user_if_found(self):
    self.nimc.register_user("Test1")
    user2 = self.nimc.register_user("Test2")
    self.nimc.register_user("Test3")
    user = self.nimc.get_user(2)
    self.assertIsInstance(user, User)
    self.assertEqual(user, user2)

  def test_get_user_returns_none_if_not_found(self):
    self.nimc.register_user("Test1")
    self.nimc.register_user("Test2")
    self.nimc.register_user("Test3")
    user = self.nimc.get_user(4)
    self.assertIsNone(user)

  def test_get_nin_returns_nin_if_found(self):
    self.nimc.register_user("Test1")
    self.nimc.register_user("Test2", "2 Bako")
    self.nimc.register_user("Test3")
    self.nimc.register_user("Test2", "4 Abiko Estate")
    user = self.nimc.get_nin("Test2")
    self.assertEqual(user, 2)
    self.assertNotEqual(user, 4)

  def test_get_nin_returns_none_if_not_found(self):
    self.nimc.register_user("Test1")
    self.nimc.register_user("Test2", "2 Bako")
    self.nimc.register_user("Test3")
    self.nimc.register_user("Test2", "4 Abiko Estate")
    user = self.nimc.get_nin("Test4")
    self.assertIsNone(user)

  def test_search_user_by_name_returns_dict_with_found_users_if_found(self):
    self.nimc.register_user("Test1")
    user2 = self.nimc.register_user("Test2", "2 Bako")
    self.nimc.register_user("Test3")
    user4 = self.nimc.register_user("Test2 Jnr", "4 Abiko Estate")
    users = self.nimc.search_user_by_name("Test2")
    self.assertEqual(len(users), 2)
    self.assertDictEqual(users, {2:user2, 4:user4})


class AccountTest(TestCase):
  def setUp(self) -> None:
    self.user = User("User", 1)
    self.account = Account(self.user, 1)

  def test_account_no_not_editable(self):
    with self.assertRaises(NotImplementedError):
      self.account.account_no = 2

  def test_account_user_not_editable(self):
    user = User("Test", 2)
    with self.assertRaises(NotImplementedError):
      self.account.user = user
  
  def test_account_balance_not_directly_editable(self):
    with self.assertRaises(AttributeError):
      self.account.balance = 200
  
  def test_account_no_property_returns_account_no(self):
    self.assertEqual(self.account.account_no, 1)
  
  def test_getaccountno_method_returns_formatted_account_no(self):
    self.assertEqual(self.account.getAccountNo(), "0000000001")
  
  def test_initial_balance_is_zero(self):
    self.assertEqual(self.account.balance, 0.0)
  
  def test_user_property_returns_account_user(self):
    self.assertEqual(self.account.user, self.user)
  
  def test_user_property_returns_account_user(self):
    self.assertIsInstance(self.account.user, User)

  def test_balance_property_returns_account_balance(self):
    self.assertEqual(self.account.balance, 0.0)

  def test_balance_property_returns_float(self):
    self.assertIsInstance(self.account.balance, float)

  def test_deposit_allows_int_and_float_values(self):
    self.account.deposit(50)
    self.account.deposit(100.0)
    self.assertEqual(self.account.balance, 150.0)
  
  def test_deposit_only_allows_int_and_float_values(self):
    with self.assertRaises(ValueError):
      self.account.deposit("50abc")

  def test_deposit_updates_account_balance(self):
    self.account.deposit(200.0)
    self.assertEqual(self.account.balance, 200.0)

  def test_deposit_zero_amount_raises_valueerror(self):
    with self.assertRaises(ValueError):
      self.account.deposit(0.0)

  def test_deposit_negative_amount_raises_valueerror(self):
    with self.assertRaises(ValueError):
      self.account.deposit(-200.0)
  
  def test_withdraw_allows_int_and_float_values(self):
    self.account.deposit(200.0)
    self.account.withdraw(50)
    self.account.withdraw(100.0)
    self.assertEqual(self.account.balance, 50.0)
  
  def test_withdraw_only_allows_int_and_float_values(self):
    self.account.deposit(200.0)
    with self.assertRaises(ValueError):
      self.account.withdraw("50")

  def test_withdraw_updates_account_balance(self):
    self.account.deposit(200.0)
    self.account.withdraw(100.0)
    self.assertEqual(self.account.balance, 100.0)

  def test_withdraw_zero_amount_raises_valueerror(self):
    with self.assertRaises(ValueError):
      self.account.withdraw(0.0)

  def test_withdraw_negative_amount_raises_valueerror(self):
    with self.assertRaises(ValueError):
      self.account.withdraw(-200.0)

  def test_withdraw_throws_valueerror_when_balance_is_insufficent(self):
    self.account.deposit(200.0)
    with self.assertRaises(ValueError):
      self.account.withdraw(250.0)

  def test_withdraw_to_zero_balance_allowed(self):
    self.account.deposit(200.0)
    self.account.withdraw(200.0)
    self.assertEqual(self.account.balance, 0.0)

  def test_transfer_updates_account(self):
    user2 = User("Test", 2)
    acc1 = Account(user2, 2)
    self.account.deposit(200)
    self.account.transfer(acc1, 50)
    self.assertEqual(self.account.balance, 150.0)
    self.assertEqual(acc1.balance, 50.0)

  def test_transfer_throws_valueerror_if_account_instance_not_given(self):
    with self.assertRaises(ValueError):
      self.account.transfer("acc1", 50)

  def test_transfer_throws_valueerror_if_balance_not_sufficient(self):
    user2 = User("Test", 2)
    acc1 = Account(user2, 2)
    self.account.deposit(200)
    with self.assertRaises(ValueError):
      self.account.transfer(acc1, 250)

class BankTest(TestCase):
  def setUp(self) -> None:
    self.nimc = NIMC()
    self.user = self.nimc.register_user("User")
    self.bank = Bank("Sama Bank", 1000000, self.nimc)
    self.account = self.bank.create_account(self.user.nin)

  def test_create_account_returns_account_on_success(self):
    user = self.nimc.register_user("Test")
    acc = self.bank.create_account(user.nin)
    self.assertIsInstance(acc, Account)
    self.assertEqual(acc.user, user)

  def test_create_account_raises_valueerror_when_nin_is_invalid(self):
    with self.assertRaises(ValueError):
      self.bank.create_account(345)
  
  def test_get_account_returns_account_on_success(self):
    acc = self.bank.get_account(self.account.account_no)
    self.assertIsInstance(acc, Account)
    self.assertEqual(acc.user, self.user)
  
  def test_get_account_returns_none_on_failure(self):
    acc = self.bank.get_account("0012344789")
    self.assertIsNone(acc)

  