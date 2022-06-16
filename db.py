import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                username VARCHAR(40), 
                email VARCHAR(50),
                password VARCHAR(100),
                region VARCHAR(100));""")

connection.commit()

cursor.execute("""CREATE TABLE IF NOT EXISTS market(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name VARCHAR(100), 
                price INTEGER(50));""")

connection.commit()




def register_user(username, email, password, region):
    cursor.execute("""INSERT INTO users(username, email, password, region) 
                    VALUES(?,?,?,?);""", [username, email, password, region])
    connection.commit()
    return cursor.lastrowid

def login(email, password):
    cursor.execute("""SELECT id, password FROM users WHERE email = ?;""", [email])
    data = cursor.fetchone()

    if data is None:
        return False

    if password == data[1]:
        return data[0]
    else:
        return False


def get_market():
    cursor.execute()