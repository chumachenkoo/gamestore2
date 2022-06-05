from market import app
from flask import render_template, redirect, url_for, request, session
from market.forms import RegisterForm
from market.models import User, users_db, shop_db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    games = shop_db.getGames()
    # if 'email_address' in session:
    #     user_email = session['email_address']
    #     user_games = users_db.getGames(user_email)
    #     return render_template('market.html', games=shop_db.clearGames(user_games))
    # else:
    return render_template('market.html', games=games)


@app.route('/buy/<gamekey>')
def buy(gamekey):
    if 'email_address' in session:
        email_address = session.get('email_address')
        user = users_db.findUser(email_address)
        game = shop_db.extractGame(gamekey)

        user.addGame(game)
        return render_template('games.html')
    else:
        return render_template("post_login.html")


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
            return redirect(url_for('post_login'))


@app.route("/login", methods=['GET'])
def get_login():
    if 'email_address' in session:
        return redirect(url_for('market_page'))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("post_login"))


@app.route('/games')
def games():
    if 'email_address' in session:
        user_email = session['email_address']
        user_games = users_db.getGames(user_email)
        return render_template("games.html", games=user_games)
    else:
        return redirect(url_for('post_login'))