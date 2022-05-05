import sqlite3
import random


clients_create_team = """CREATE TABLE IF NOT EXISTS clients (first_name, second_name,
                       address, passport_series, passport_number,
                       phone_number, password)"""

accounts_create_team = """CREATE TABLE IF NOT EXISTS accounts (id, phone_number,
                        account_type, balance, term)"""

transactions_create_team = """CREATE TABLE IF NOT EXISTS transactions (transaction_id, 
                                                            first_id, second_id, money)"""

select_client_team = """SELECT first_name, second_name, address, passport_series, passport_number,
                      phone_number, password FROM clients WHERE phone_number = ?"""

select_account_team = """SELECT id, phone_number, account_type, balance, term
                       FROM accounts WHERE id = ?"""

select_transaction_team = """SELECT transaction_id, first_id, second_id, money, 
                             FROM transactions WHERE transaction_id = ?"""

add_to_clients_team = "insert into clients values (?, ?, ?, ?, ?, ?, ?)"

add_to_accounts_team = "insert into accounts values (?, ?, ?, ?, ?)"

add_to_transactions_team = "insert into transactions value (?, ?, ?, ?)"

update_account_balance = "update accounts set balance = ? where id = ?"


class BankDataBase:
    def __init__(self):
        self.connection = sqlite3.connect("bank.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(clients_create_team)
        self.cursor.execute(accounts_create_team)
        self.cursor.execute(transactions_create_team)

    def new_account_id(self):
        result_id = random.randint(10 ** 16, 10 ** 17 - 1)
        while self.get_account_params(result_id) is not None:
            result_id = random.randint(10 ** 16, 10 ** 17 - 1)
        return result_id

    def add_new_client(self, params):
        self.cursor.execute(add_to_clients_team, params)
        self.connection.commit()

    def add_new_account(self, params):
        self.cursor.execute(add_to_accounts_team, params)
        self.connection.commit()

    def get_client_params(self, phone_number):
        row = self.cursor.execute(select_client_team, (phone_number,)).fetchall()
        if len(row):
            return row[0]

    def get_account_params(self, account_id):
        row = self.cursor.execute(select_account_team, (account_id,)).fetchall()
        if len(row):
            return row[0]

    def account_exists(self, id):
        return self.get_account_params(id) is not None

    def client_exists(self, phone_number):
        return self.get_client_params(phone_number) is not None

    def set_balance(self, new_balance, id):
        self.cursor.execute(update_account_balance, (new_balance, id))
        self.connection.commit()

    def close(self):
        self.connection.close()
