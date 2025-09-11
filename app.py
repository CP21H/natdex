from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = "testing_key"

##############################
#                            #
#      DATABASE CREATION     #
#                            #
##############################
# DATABASE CREATION
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute(
            '''CREATE TABLE IF NOT EXISTS users(
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT, 
            password TEXT);''')
        conn.commit()

init_db()


##############################
#                            #
#       LOGIN / LOGOUT       #
#                            #
##############################
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    messages = []
    logged_in = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            messages.append("Invalid username and/or password")
        else:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT username, password FROM users WHERE username = ? AND password = ?", (username,password))
                user = cursor.fetchone()

                if user:
                    session['username'] = user[0]
                    logged_in = True
                    session['logged_in'] = True
                    session.permanent = False
                    return render_template('index.html', logged_in=logged_in, username=session['username'])
                else:
                    messages.append("Invalid username and/or password")

    return render_template('login.html', messages=messages)


@app.route('/logout.html', methods=['GET', 'POST'])
def logout():
    logged_in = session.get('logged_in')
    username = session.get('username')
    return render_template('logout.html', logged_in=logged_in, username=username)


@app.route('logout_confirm')
def logout_confirm():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('login'))


##############################
#                            #
#       SIGN UP              #
#                            #
##############################
@app.route('/signup.html', methods=['GET', 'POST'])
def signup():
    messages = []
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirm = request.form['password-confirm']

        # VALIDATION CHECKING
        if not username:
            messages.append("Username invalid")
        if not password:
            messages.append("Provide a password")
        if password != password_confirm:
            messages.append("Passwords do not match")
        # CHECK IF THE USERNAME IS IN USE ALREADY
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
            user_check = cursor.fetchone()
            if user_check:
                messages.append("Username already exists")

        # MESSAGES LIST = EMPTY, ZERO ERRORS
        if not messages:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            messages.append("Account created! Please log in to continue.")

    return render_template('signup.html', messages=messages)


##############################
#                            #
#           INDEX            #
#                            #
##############################
@app.route('/')
def index():
    logged_in = session.get('logged_in')
    username = session.get('username')
    return render_template('index.html', logged_in=logged_in, username=username)


if __name__ == '__main__':
    app.run()
