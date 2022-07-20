from market import app
from flask import render_template, redirect, url_for, request, session, flash
from market.forms import RegisterForm
import database
import key_generator


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    games_catalog = database.get_market_games()
    return render_template('market.html', games=games_catalog)


@app.route('/buy/<game_id>')
def buy(game_id):
    user_id = session.get('id')
    if user_id is not None:
        data = database.find_regions(user_id, game_id)
        if data[0][0] != data[0][1]:
            serial = key_generator.generate()
            database.register_game(game_id, user_id, serial)
            return redirect(url_for('games'))
        else:
            flash('Game is banned in your region', 'info')
            return redirect(url_for('market_page'))
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

        database.register_user(username, email_address, password, region)

        return redirect(url_for('get_login'))


@app.route("/login", methods=['POST'])
def post_login():
    if request.method == 'POST':
        session.permanent = True
        email_address = request.form['email']
        password = request.form['password']

        user_data = database.get_user_by_email(email_address)
        if user_data is not None:
            if password == user_data[3]:
                session['id'] = user_data[0]
                return redirect(url_for('market_page'))

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
    user_id = session.get('id')
    if user_id is not None:
        user_games = database.get_user_games(user_id)
        return render_template("games.html", games=user_games)
    else:
        return redirect(url_for('get_login'))