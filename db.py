import sqlite3
import os
import random


clients_create_team = "CREATE TABLE clients (first_name TEXT, second_name TEXT,\
               address TEXT, passport_serie INTEGER, passport_number INTEGER,\
               phone_number INTEGER, password TEXT, verified BOOL)"

accounts_create_team = "CREATE TABLE accounts (id INTEGER, phone_number INTEGER,\
                        type TEXT, money_amount INTEGER, comission INTEGER, term TEXT)"

select_client_team = "SELECT first_name, second_name, address, passport_serie,\
                      passport_number, phone_number, password, verified\
                      WHERE phone_number = ?"

select_account_team = "SELECT id, phone_number, type, money_amount, comission, term\
                       FROM accounts WHERE id = ?"


def new_id():
    result_id = random.randint(10 ** 16, 10 ** 17 - 1)
    while select_account_team(result_id) is not None:
        result_id = random.randint(10 ** 16, 10 ** 17 - 1)
    return result_id


def get_client_params(phone_number):
    row = client_cursor.execute(select_client_team, (phone_number)).fetchall()
    if len(row):
        return row[0]


def get_account_params(account_id):
    row = accounts_cursor.execute(select_account_team, (account_id)).fetchall()
    if len(row):
        return row[0]


if __name__ == '__main__':
    clients_connection = sqlite3.connect("clients.db")
    client_cursor = clients_connection.cursor()
    if not os.path.isfile('clients.db'):
        client_cursor.execute(create_team)

    accounts_connection = sqlite3.connect("accounts.db")
    accounts_cursor = accounts_connection.cursor()
    if not os.path.isfile('accounts.db'):
        accounts_cursor.execute()
