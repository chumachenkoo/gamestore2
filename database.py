import sqlite3

connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


def register_user(username, email, pwd, region):
    cursor.execute("""INSERT INTO users(username, email, password, region)
                        VALUES (?, ?, ?, ?)""", (username, email, pwd, region))
    connection.commit()


def get_user_by_email(email):
    cursor.execute("""SELECT * FROM users WHERE email = ?""", (email,))
    data = cursor.fetchone()
    return data


def get_market_games():
    games = []
    catalog = cursor.execute("""SELECT * FROM market;""").fetchall()
    for item in catalog:
        l = list(item)
        game_id = l[0]
        cursor.execute("""SELECT country FROM restricted WHERE market_id = ?;""", (game_id, ))
        rest = cursor.fetchall()
        r = []
        for i in rest:
            r.append(i[0])
        l.append(r)
        games.append(l)

    return games


def register_game(market_id, user_id, serial):
    cursor.execute("""INSERT INTO games(market_id, user_id, serial) VALUES(?,?,?);""", (market_id, user_id, serial))
    connection.commit()


def get_user_games(user_id):
    cursor.execute("""SELECT market.name, market.price, games.serial FROM games 
    JOIN market ON games.market_id = market.id 
    JOIN users ON games.user_id = users.id
    WHERE users.id = ?;""", (user_id, ))
    return cursor.fetchall()


def find_regions(user_id, game_id):
    cursor.execute("""SELECT users.region, restricted.country FROM users JOIN restricted 
                    WHERE users.id = ? AND restricted.market_id = ?;""", (user_id, game_id))
    return cursor.fetchall()