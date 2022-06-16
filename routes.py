from market import app
from flask import render_template, redirect, url_for, request, session
from market.forms import RegisterForm
from market import db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_page():
    user_id = session.get('id')

    games = db.get_market()

    return render_template('market.html', games=games)


@app.route('/buy/<game_name>')
def buy(game_name):
    if 'id' in session:
        user_id = session.get('id')



        # return redirect(url_for('games'))
        return str(user_id)
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

        user_id = db.register_user(username, email_address, password, region)
        session['id'] = user_id

        return redirect(url_for('market_page'))


@app.route("/login", methods=['POST'])
def post_login():
    if request.method == 'POST':
        session.permanent = True
        email_address = request.form['email']
        password = request.form['password']
        result = db.login(email_address, password)

        if result:
            session['id'] = result
            return redirect(url_for('market_page'))
        else:
            return redirect(url_for('get_login'))




@app.route("/login", methods=['GET'])
def get_login():
    if 'id' in session:
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
        return render_template("games.html", games=user_games)
    else:
        return redirect(url_for('get_login'))