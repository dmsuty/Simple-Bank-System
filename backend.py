from abc import ABC, abstractmethod
from datetime import date, timedelta
from db import BankDataBase
import constants


"======================= Clients =============================================="


class Client:
    def __init__(self, params):
        self.first_name = params[0]
        self.second_name = params[1]
        self.address = params[2]
        self.passport_series = params[3]
        self.passport_number = params[4]
        self.phone_number = params[5]
        self.password = params[6]

    def is_verified(self):
        return self.address and self.passport_series and self.passport_number

    def params(self):
        return (self.first_name, self.second_name, self.address,
                self.passport_series, self.passport_number, self.phone_number, self.password)


"======================== there are accounts =================================="


class AbstractAccount(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def withdraw(self, money_amount) -> int:
        pass

    @abstractmethod
    def deposit(self, money_amount):
        pass

    @abstractmethod
    def get_id(self):
        pass


class Deposit(AbstractAccount):
    @abstractmethod
    def get_term(self) -> date:
        pass


class Credit(AbstractAccount):
    @abstractmethod
    def get_debt(self) -> int:
        pass


class Debit(AbstractAccount):
    pass


class KazachestvoDeposit(Deposit):
    def __init__(self, client, balance):
        self.max_deposit = self.max_deposit(client)
        if balance > self.max_deposit:
            raise Exception
        self.balance = balance
        self.phone_number = client.phone_number
        self.term = self.new_deposit_term()
        self.id = bank_data_base.new_account_id()

    def get_term(self):
        return self.term

    def get_id(self):
        return self.id

    def withdraw(self,  write_off):
        if date.today() < self.term:
            raise Exception
        if self.balance < write_off:
            raise Exception
        self.balance -= write_off

    def deposit(self, deposit_amount):
        if self.balance + deposit_amount > self.max_deposit:
            raise Exception
        self.balance += deposit_amount

    @staticmethod
    def new_deposit_term():
        return date.today() + timedelta(days=500)

    @staticmethod
    def max_deposit(client):
        if client.is_verified():
            return constants.MaxKazachestvoVerifiedDeposit
        return constants.MaxKazachestvoNotVerifiedDeposit


class KazachestvoCredit(Credit):
    def __init__(self, client):
        self.balance = 0
        self.phone_number = client.phone_number
        self.id = bank_data_base.new_account_id()
        if client.is_verified():
            self.max_credit = constants.MaxKazachestvoVerifiedCredit
        else:
            self.max_credit = constants.MaxKazachestvoNotVerifiedCredit

    def withdraw(self, write_off):
        if -(self.balance - write_off) > self.max_credit:
            raise Exception
        if self.balance < write_off:
            pass
        self.balance -= write_off

    def get_id(self):
        return self.id

    def deposit(self, deposit_amount):
        self.balance += deposit_amount

    def get_debt(self) -> int:
        return max(0, -self.balance)


class KazachestvoDebit(Debit):
    def __init__(self, client):
        self.max_balance = self.max_balance(client)
        self.balance = 0
        self.phone_number = client.phone_number
        self.id = bank_data_base.new_account_id()

    def withdraw(self,  write_off):
        if self.balance < write_off:
            raise Exception
        self.balance -= write_off

    def get_id(self):
        return self.id

    def deposit(self, deposit_amount):
        if self.balance + deposit_amount > self.max_balance():
            raise Exception
        self.balance += deposit_amount

    @staticmethod
    def max_balance(client):
        if client.is_verified():
            return constants.MaxKazachestvoVerifiedDebitBalance
        return constants.MaxKazachestvoNotVerifiedDebitBalance


"======================== there are fabrics ==================================="


class AbstractAccountFactory(ABC):
    @staticmethod
    def create_deposit(self, client, balance) -> Deposit:
        pass

    @staticmethod
    def create_credit(self, client) -> Credit:
        pass

    @staticmethod
    def create_debit(self, client) -> Debit:
        pass


class KazachestvoFactory(AbstractAccountFactory):
    @staticmethod
    def create_deposit(self, client, balance) -> Deposit:
        return KazachestvoDeposit(client, balance)

    @staticmethod
    def create_credit(self, client) -> Credit:
        return KazachestvoCredit(client)

    @staticmethod
    def create_debit(self, client) -> Debit:
        return KazachestvoDebit(client)


"================ Transaction ========================="

class Transaction:
    def __init__(self, first_account, second_account, money):
        bank_data_base.add_new_transaction()


bank_data_base = BankDataBase()
