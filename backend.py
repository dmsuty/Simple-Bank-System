from abc import ABC, abstractmethod
from datetime import date, timedelta
from db import BankDataBase
import constants


def str_to_date(strdate):
    y, m, h = map(int, strdate.split(':'))
    return timedelta(y, m, h)


"======================= Clients =============================================="


class Client:   # make Builder later TODO
    def __init__(self, params):
        self.first_name = params[0]
        self.second_name = params[1]
        self.address = params[2]
        self.passport_series = params[3]
        self.passport_number = params[4]
        self.phone_number = params[5]
        self.password = params[6]
        self.write_to_bd()

    def change_phone_number(self):  # TODO
        pass

    def change_password(self):  # TODO
        pass

    def change_address(self, new_address):  # TODO
        pass

    def add_passport(self):    # TODO
        if self.passport_number == '':
            raise Exception
        pass

    def is_verified(self):
        return self.address and self.passport_series and self.passport_number

    def bd_params(self):
        return (self.first_name, self.second_name, self.address,
                self.passport_series, self.passport_number, self.phone_number, self.password)

    def write_to_bd(self):
        if bank_data_base.get_client_params(self.phone_number) is None:
            bank_data_base.add_new_client(self.bd_params())

    @staticmethod
    def get_client(phone_number):
        return Client(bank_data_base.get_client_params(phone_number))


"======================== there are accounts =================================="


class Account(ABC):
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

    @staticmethod
    def get_account(account_id):
        params = bank_data_base.get_account_params(account_id)
        type, bank = params[2:4]
        if type == 'credit' and bank == 'Kazachestvo':
            return KazachestvoCredit.params_to_account(params)
        if type == 'debit' and bank == 'Kazachestvo':
            return KazachestvoDebit.params_to_account(params)
        if type == 'deposit' and bank == 'Kazachestvo':
            return KazachestvoDeposit.params_to_account(params)
        pass    # TODO may be other banks


class Deposit(Account):
    @abstractmethod
    def get_term(self) -> date:
        pass


class Credit(Account):
    @abstractmethod
    def get_debt(self) -> int:
        pass


class Debit(Account):
    pass


class KazachestvoDeposit(Deposit):
    def __init__(self, client=None, balance=None):
        if client is not None:
            self.max_deposit = self.max_deposit(client)
            if balance > self.max_deposit:
                raise Exception
            self.balance = balance
            self.phone_number = client.phone_number
            self.term = self.new_deposit_term()
            self.id = bank_data_base.new_account_id()
            self.type = 'deposit'
            self.bank = 'Kazachestvo'
            self.write_to_bd()

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
        self.write_to_bd()

    def deposit(self, deposit_amount):
        if self.balance + deposit_amount > self.max_deposit:
            raise Exception
        self.balance += deposit_amount
        self.write_to_bd()

    def bd_params(self):
        return self.id, self.phone_number, self.type, self.bank, self.balance, str(self.term)

    def write_to_bd(self):
        if bank_data_base.get_account_params(self.id) is None:
            bank_data_base.add_new_account(self.bd_params())
        else:
            bank_data_base.set_balance(self.balance, self.id)

    def max_deposit(self):
        client = Client.get_client(self.phone_number)
        if client.is_verified():
            return constants.MaxKazachestvoVerifiedDeposit
        return constants.MaxKazachestvoNotVerifiedDeposit

    @staticmethod
    def new_deposit_term():
        return date.today() + timedelta(days=500)


    @staticmethod
    def params_to_account(account_params):
        account = KazachestvoDeposit()
        account.account_id = account_params[0]
        account.phone_number = account_params[1]
        account.type = account_params[2]
        account.balance = account_params[3]
        account.term = str_to_date(account_params[4])
        return account


class KazachestvoCredit(Credit):
    def __init__(self, client=None):
        if client is not None:
            self.balance = 0
            self.phone_number = client.phone_number
            self.id = bank_data_base.new_account_id()
            self.type = 'credit'
            self.bank = "Kazachestvo"
            self.write_to_bd()

    def withdraw(self, write_off):
        if -(self.balance - write_off) > self.max_credit():
            raise Exception
        if self.balance < write_off:
            pass
        self.balance -= write_off
        self.write_to_bd()

    def deposit(self, deposit_amount):
        self.balance += deposit_amount
        self.write_to_bd()

    def get_id(self):
        return self.id

    def get_debt(self) -> int:
        return max(0, -self.balance)

    def bd_params(self):
        return self.id, self.phone_number, self.type, self.bank, self.balance, str(timedelta())

    def write_to_bd(self):
        if bank_data_base.get_account_params(self.id) is None:
            bank_data_base.add_new_account(self.bd_params())
        else:
            bank_data_base.set_balance(self.balance, self.id)

    def max_credit(self):
        client = Client.get_client(self.phone_number)
        if client.is_verified():
            return constants.MaxKazachestvoVerifiedCredit
        return constants.MaxKazachestvoNotVerifiedCredit

    @staticmethod
    def params_to_account(account_params):
        account = KazachestvoCredit()
        account.account_id = account_params[0]
        account.phone_number = account_params[1]
        account.type = account_params[2]
        account.bank = account_params[3]
        account.balance = account_params[4]
        account.term = str_to_date(account_params[5])
        return account


class KazachestvoDebit(Debit):
    def __init__(self, client=None):
        if client is not None:
            self.balance = 0
            self.phone_number = client.phone_number
            self.type = "debit"
            self.bank = "Kazachestvo"
            self.account_id = bank_data_base.new_account_id()
            self.write_to_bd()

    def withdraw(self,  write_off):
        if self.balance < write_off:
            raise Exception
        self.balance -= write_off
        self.write_to_bd()

    def deposit(self, deposit_amount):
        if self.balance + deposit_amount > self.max_balance():
            raise Exception
        self.balance += deposit_amount
        self.write_to_bd()

    def get_id(self):
        return self.account_id

    def bd_params(self):
        return self.account_id, self.phone_number, self.type, self.bank, self.balance, str(timedelta())

    def write_to_bd(self):
        if not bank_data_base.account_exists(self.account_id):
            bank_data_base.add_new_account(self.bd_params())
        else:
            bank_data_base.set_balance(self.balance, self.account_id)

    def max_balance(self):
        client = Client.get_client(self.phone_number)
        if client.is_verified():
            return constants.MaxKazachestvoVerifiedDebitBalance
        return constants.MaxKazachestvoNotVerifiedDebitBalance

    @staticmethod
    def params_to_account(account_params):
        account = KazachestvoDebit()
        account.account_id = account_params[0]
        account.phone_number = account_params[1]
        account.type = account_params[2]
        account.bank = account_params[3]
        account.balance = account_params[4]
        account.term = str_to_date(account_params[5])
        return account


"======================== there are fabrics ==================================="


class AbstractAccountFactory(ABC):
    @staticmethod
    def create_deposit(client, balance) -> Deposit:
        pass

    @staticmethod
    def create_credit(client) -> Credit:
        pass

    @staticmethod
    def create_debit(client) -> Debit:
        pass


class KazachestvoFactory(AbstractAccountFactory):
    @staticmethod
    def create_deposit(client, balance) -> Deposit:
        return KazachestvoDeposit(client, balance)

    @staticmethod
    def create_credit(client) -> Credit:
        return KazachestvoCredit(client)

    @staticmethod
    def create_debit(client) -> Debit:
        return KazachestvoDebit(client)


"================ Transaction ========================="


class Transaction:
    def __init__(self, creditor, receiver, money, status='confirmed'):
        self.transaction_id = bank_data_base.new_transaction_id()
        self.creditor_id = creditor.account_id
        self.receiver_id = receiver.account_id
        self.summ = money
        self.status = status
        self.write_to_bd()
        creditor.withdraw(money)
        receiver.deposit(money)

    def bd_params(self):
        return self.transaction_id, self.creditor_id, self.receiver_id, self.summ, self.status

    def write_to_bd(self):
        if bank_data_base.get_transaction_params(self.transaction_id) is None:
            bank_data_base.add_new_transaction(self.bd_params())

    @staticmethod
    def get_creditor(transaction_id):
        params = bank_data_base.get_transaction_params(transaction_id)
        return params[1]

    @staticmethod
    def get_receiver(transaction_id):
        params = bank_data_base.get_transaction_params(transaction_id)
        return params[2]

    @staticmethod
    def get_summ(transaction_id):
        params = bank_data_base.get_transaction_params(transaction_id)
        return params[3]

    @staticmethod
    def cancel(transaction_id):
        creditor = Account.get_account(Transaction.get_creditor(transaction_id))
        receiver = Account.get_account(Transaction.get_receiver(transaction_id))
        Transaction(receiver, creditor, Transaction.get_summ(transaction_id), 'cancelled')


# def call_collector(bad_client):
#     pass - should make it later


bank_data_base = BankDataBase()