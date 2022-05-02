from abc import ABC, abstractmethod
from datetime import date
import constants
import sqlite3
import db


"======================= Clients =============================================="


class Client:
    def __init__(self, params):
        self.first_name = params[0]
        self.second_name = params[1]
        self.address = params[2]
        self.passport_serie = params[3]
        self.passport_number = params[4]
        self.phone_number = params[5]

    def is_verified(self):
        pass


def get_client(phone_number):
    return Client(db.get_client_params(phone_number))


def get_account(account_id):
    account_data = db.get_account_params(account_id)


"======================== there are accounts =================================="


class AbstractAccount(ABC):
    @abstractmethod
    def __init__(self, money_amount):
       pass 
    
    @abstractmethod
    def withdraw(self, money_amount) -> int:
        pass

    @abstractmethod
    def deposit(self, money_amount):
        pass


class Deposit(AbstractAccount):
    @abstractmethod
    def get_term(self) -> date:
        pass


class Credit(AbstractAccount):
    @abstractmethod
    def get_limit(self) -> int:
        pass

    @abstractmethod
    def get_comission(self) -> float:
        pass


class Debit(AbstractAccount):
    pass


class KazachestvoDeposit(Deposit):
    def __init__(client, balance):
        self.max_deposit = max_deposit(client)
        if balance > max_deposit:
            raise Exception
        self.balance = balance
        self.phone_number = client.phone_number
        self.term = self.new_deposit_term()
        self.id = db.new_id()

    def get_term(self):
        return self.term

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
    def new_deposit_term(date):
        return date.today()

    @staticmethod
    def max_deposit(client):
        return constants.MaxKazachestvoVerifiedDeposit if client.is_verified()\
                               else constants.MaxKazachestvoNotVerifiedDeposit


class KazachestvoCredit(Credit):
    def __init__(client):
        self.balance = 0
        self.phone_number = client.phone_number
        self.id = db.new_id()
        if client.is_verified():
            self.max_credit = constants.MaxKazachestvoVerifiedCredit
        else:
            self.max_credit = constants.MaxKazachestvoNotKazachestvoCredit

    def withdraw(self, write_off):
        if abs(self.balance - write_off) > self.max_credit:
            raise Exception    
        self.balance -= write_off

    def deposit(self, deposit_amount):
        self.balance += deposit_amount

    def get_debt(self) -> int:
        return max(0, -self.balance)


class KazachestvoDebit(Debit):
    def __init__(client):
        self.balance = 0
        self.phone_number = client.phone_number
        self.id = db.new_id()

    def withdraw(self,  write_off):
        if self.balance < write_off:
            raise Exception
        self.balance -= write_off

    def deposit(self, deposit_amount):
        self.balance += deposit_amount



# class BetaDeposit(Deposit):
#     def __init__(client):


# class BetaCredit(Credit):
#     pass

# class BetaDebit(Debit):
#     pass


"======================== there are fabrics ==================================="


class AbstractAccountFactory(ABC):
    def create_deposit(self) -> Deposit:
        pass #TODO

    def create_credit(self) -> Credit:
        pass #TODO

    def create_debit(self) -> Debit:
        pass #TODO


class KazachestvoFactory(AbstractAccountFactory):
    def create_deposit(self, client) -> Deposit:
        pass #TODO


class BetaFactory(AbstractAccountFactory):
    pass
