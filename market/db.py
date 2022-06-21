import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(40),
                    email VARCHAR(50),
                    password VARCHAR(100),
                    region VARCHAR(100));""")

cursor.execute("""CREATE TABLE IF NOT EXISTS market(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game VARCHAR(100),
                price INTEGER,
                banned_region VARCHAR(50)
            );""")

cursor.execute("""CREATE TABLE IF NOT EXISTS games(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (game_id) REFERENCES market(id)
            );""")

connection.commit()


def register_user(username, email, password, region):
    cursor.execute("""INSERT INTO users(username, email, password, region) 
                    VALUES(?, ?, ?, ?);""", [username, email, password, region])
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
    cursor.execute("SELECT * FROM market;")
    data = cursor.fetchall()
    return data


def get_user_games(user_id):
    cursor.execute(f"SELECT users.id, username, market.name FROM games INNER JOIN market, users ON games.game_id = market.id AND games.user_id = users.id;")
    data = cursor.fetchall()
    return data[user_id]
