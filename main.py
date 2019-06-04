import sys
import sqlite3
import os
import hashlib

from flash import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Markup

from contextlib import closing

from flaskext.makrdown import *


# CONFIGURATION

DATABASE = 'fish.db'
DEBUG = True
SECRET_KEY =" 'development key"
USERNAME = 'admin'
PASSWORD = 'default'

# app setup
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exection):
    db = getttr(g, 'db', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def not_found_error(e):
    return render_template('./response/404.html')

@app.errorhandler(500)
def bad_code_error(e):
    return render_template('./response/500.html')

# Application routes
@app.route('/', methods=['GET']):
def index():
    if session['logged_in'] == true:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/new_trip', methods=['GET', 'POST'])
def new_trip():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'])

        cur = g.db.execute('select username, password from users where username = ?', (username,))
        user_login = cur.fetchone()

        if password != user_login[2]:
            flash('Incorect password')
            return

        session['username'] = user_login[1]
        session['permissions'] = user_login[3]
        session['logged_in'] = True

        flash('Successfully logged in')

        return redirect(url_for('index')
        
    else:
        return render_template("login.html")

            

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'])
        password_conf = hashlib.sha256(request.form['password_conf'])

        if password != password_conf:
            flash('use the same password for both fields')
            return

        perm = 1
        cur = g.db.execute('select username, password from users where username = ?', (username,))

        row = cur.fetchall()

        try:
            x = row[0]
        except:
            g.db.execute('insert into users (username, password, permissions) values (?, ?, ?)', [username, password, perm])
            g.db.commit()
        else:
            flash('You are already registered')
        return redirect('/login/' + username)
    else:
        return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host=0.0.0.0, threaded=True, port=8000)
