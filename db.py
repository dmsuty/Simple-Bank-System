import sqlite3
import random


clients_create_team = """CREATE TABLE IF NOT EXISTS clients (first_name, second_name,
                       address, passport_series, passport_number,
                       phone_number, password)"""

accounts_create_team = """CREATE TABLE IF NOT EXISTS accounts (account_id, phone_number,
                        account_type, bank, balance, term)"""

transactions_create_team = """CREATE TABLE IF NOT EXISTS transactions (transaction_id, 
                                                            creditor_id, receiver_id, summ, status)"""

select_client_team = """SELECT first_name, second_name, address, passport_series, passport_number,
                      phone_number, password FROM clients WHERE phone_number = ?"""

select_account_team = """SELECT account_id, phone_number, account_type, bank, balance, term
                       FROM accounts WHERE account_id = ?"""

select_transaction_team = """SELECT transaction_id, creditor_id, receiver_id, summ, status 
                             FROM transactions WHERE transaction_id = ?"""

add_to_clients_team = "insert into clients values (?, ?, ?, ?, ?, ?, ?)"

add_to_accounts_team = "insert into accounts values (?, ?, ?, ?, ?, ?)"

add_to_transactions_team = "insert into transactions values (?, ?, ?, ?, ?)"

change_account_balance = "update accounts set balance = ? where account_id = ?"

change_transaction_status = "update transactions set status = ? where transaction_id = ?"


class BankDataBase:
    def __init__(self):
        self.connection = sqlite3.connect("bank.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(clients_create_team)
        self.cursor.execute(accounts_create_team)
        self.cursor.execute(transactions_create_team)

    def new_account_id(self):
        result_id = self.random_int(12)
        while self.get_account_params(result_id) is not None:
            result_id = self.random_int(12)
        return result_id

    def new_transaction_id(self):
        result_id = self.random_int(16)
        while self.get_transaction_params(result_id) is not None:
            result_id = self.random_int(16)
        return result_id

    def add_new_client(self, params):
        self.cursor.execute(add_to_clients_team, params)
        self.connection.commit()

    def add_new_account(self, params):
        self.cursor.execute(add_to_accounts_team, params)
        self.connection.commit()

    def add_new_transaction(self, params):
        self.cursor.execute(add_to_transactions_team, params)
        self.connection.commit()

    def get_client_params(self, phone_number):
        row = self.cursor.execute(select_client_team, (phone_number,)).fetchall()
        if len(row):
            return row[0]

    def get_account_params(self, account_id):
        row = self.cursor.execute(select_account_team, (account_id,)).fetchall()
        if len(row):
            return row[0]

    def get_transaction_params(self, transaction_id):
        row = self.cursor.execute(select_transaction_team, (transaction_id, )).fetchall()
        if len(row):
            return row[0]

    def account_exists(self, account_id):
        return self.get_account_params(account_id) is not None

    def client_exists(self, phone_number):
        return self.get_client_params(phone_number) is not None

    def transaction_exists(self, transaction_id):
        return self.get_transaction_params(transaction_id) is not None

    def set_balance(self, new_balance, account_id):
        self.cursor.execute(change_account_balance, (new_balance, account_id))
        self.connection.commit()

    def set_transaction_status(self, new_status, transaction_id):
        self.cursor.execute(change_transaction_status, (new_status, transaction_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

    @staticmethod
    def random_int(count_of_digits):
        return random.randint(10 ** count_of_digits, 10 ** (count_of_digits + 1) - 1)
