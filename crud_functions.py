import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Эта функция создаёт таблицу Products, если она ещё не создана

def initiate_db():
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INT NOT NULL
)
''')
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INT NOT NULL,
balance INT NOT NULL
)
''')

    connection.commit()

# Эта функция возвращает все записи из таблицы Products

def get_all_products():
    connection_1 = sqlite3.connect('database.db')
    cursor_1 = connection_1.cursor()
    cursor_1.execute('SELECT * FROM Products')
    products = cursor_1.fetchall()
    connection_1.close()
    return products

# Эта функция заполняет нашу базу данных продуктами. Используется один раз.

def add_products():
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)',
                       (f'Продукт{i}', f'Описание{i}', i * 100))

    connection.commit()

# Эта функция добавляет нового пользователя в таблицу Users

def add_user(username, email, age):
    connection_2 = sqlite3.connect('database.db')
    cursor_2 = connection_2.cursor()
    cursor_2.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (username, email, age, 1000))

    connection_2.commit()
    connection_2.close()

# Эта функция проверяет, существует ли пользователь с именем username.
# Если существует, возвращает значение True, иначе False

def is_included(username):
    connection_3 = sqlite3.connect('database.db')
    cursor_3 = connection_3.cursor()
    users = cursor_3.execute('SELECT username From Users WHERE username = ?', (username,)).fetchone()

    if users is not None:
        connection_3.close()
        return True
    else:
        connection_3.close()
        return False

# Запускаем один раз при создании и заполнении базы данных Products
# initiate_db()
# add_products()

connection.commit()
connection.close()

