
class User:

    games = []

    def __init__(self, username, email_address, password, region, budget=0):
        self.username = username
        self.password = password
        self.email_address = email_address
        self.region = region
        self.budget = budget

    def addGame(self, game):
        self.games.append(game)

    def getGames(self):
        return self.games


    def __repr__(self):
        return f"User => {self.username}:{self.email_address}"


class Game:

    def __init__(self, key, name, price, banned_region=None):
        self.key = key
        self.name = name
        self.price = price
        self.banned_region = banned_region

    def __repr__(self):
        return f"Game => {self.name}:{self.price}({self.key}, {self.banned_region}"


class UsersDB:

    db = []

    def addUser(self, user: User):
        self.db.append(user)

    def getUsers(self):
        return self.db

    def findUser(self, email_address):
        for i in self.db:
            if i.email_address == email_address:
                return i

    def getGames(self, email_address):
        for user in UsersDB.db:
            if user.email_address == email_address:
                return user.games
        else:
            return 'No user games!'


# class Shop:
#     db = []
#
#     def addGame(self, game: Game):
#         self.db.append(game)
#
#     def getGames(self):
#         return self.db
#
#     def extractGame(self, key):
#         index = 0
#         for i in self.db:
#             if i.key == key:
#                 break
#             else:
#                 index += 1
#         return self.db.pop(index)

class Catalog:
    catalog = [
        {   'name': 'GTA',
            'restricted': 'Ukraine',
            'price': 150
        },
        {   'name': 'StarWars',
            'restricted': 'Canada',
            'price': 150
        },
        {   'name': 'NFS',
            'restricted': 'Poland',
            'price': 150
        },
        {   'name': 'WarThunder',
            'restricted': 'Czech Republic',
            'price': 150
        },
        {   'name': 'Lego',
            'restricted': 'Poland',
            'price': 150
        }
    ]

    def getCatalog(self):
        return self.catalog

    def findGame(self, name):
        for i in self.catalog:
            if i['name'] == name:
                return i

    def getFiltered(self, purchased):
        res = []
        for game in self.catalog:
            if game['name'] not in purchased:
                res.append(game)
        return res


users_db = UsersDB()
catalog = Catalog()
# shop_db = Shop()

# shop_db.addGame(Game("key1", "GTA", 150, 'Ukraine'))
# shop_db.addGame(Game("key2", "StarWars", 90, 'Canada'))
# shop_db.addGame(Game("key3", "NFS", 200, 'Poland'))
# shop_db.addGame(Game("key4", "WarThunder", 300, 'Czech Republic'))
# shop_db.addGame(Game("key5", "Lego", 250, 'Poland'))

u1 = User("Maksim", 'maksim@gmail.com', "1234", 'Canada', 1500)
u1.addGame(Game("key1", "GTA", 150))
u1.addGame(Game("key2", "StarWars", 90))
u1.addGame(Game("key4", "WarThunder", 300))

users_db.addUser(u1)

