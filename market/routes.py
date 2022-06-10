from market import app
from flask import render_template, redirect, url_for, request, session
from market.forms import RegisterForm
from market.models import User, users_db, catalog, Game
from random import randint


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    user_email = session.get('email_address')

    if user_email is not None:
        purchased = []
        for game in users_db.findUser(user_email).getGames():
            purchased.append(game.name)

        res = catalog.getFiltered(purchased)

        return render_template('market.html', games=res)

    return render_template('market.html', games=catalog.getCatalog())


@app.route('/buy/<game_name>')
def buy(game_name):
    if 'email_address' in session:
        email_address = session.get('email_address')
        user = users_db.findUser(email_address)

        key = str(randint(10000, 99000))

        game = Game(key, game_name, catalog.findGame(game_name)['price'], catalog.findGame(game_name)['restricted'])

        user.addGame(game)
        return redirect(url_for('games'))
    else:
        return redirect(url_for('get_login'))


@app.route('/register', methods=['POST', 'GET'])
def register_page():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('register.html', form=form)
    else:
        username = request.form.get('username')
        email_address = request.form.get('email_address')
        password = request.form.get('password1')
        region = request.form.get('region')

        u = User(username, email_address, password, region)
        users_db.addUser(u)

        session['email_address'] = u.email_address
        return redirect(url_for('market_page'))


@app.route("/login", methods=['POST'])
def post_login():
    if request.method == 'POST':
        session.permanent = True
        email_address = request.form['email']
        password = request.form['password']

        user_data = users_db.findUser(email_address)

        if user_data is not None:
            if password == user_data.password:
                session['email_address'] = email_address
                return redirect(url_for('market_page'))
        else:
            return redirect(url_for('get_login'))


@app.route("/login", methods=['GET'])
def get_login():
    if 'email_address' in session:
        return redirect(url_for('market_page'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("get_login"))


@app.route('/games')
def games():
    if 'email_address' in session:
        user_email = session['email_address']
        user_games = users_db.findUser(user_email).getGames()
        return render_template("games.html", games=user_games)
    else:
        return redirect(url_for('get_login'))