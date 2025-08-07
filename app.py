from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3

app = Flask(__name__)

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
                    session['username'] = user[1]
                    return redirect(url_for('index'))
                else:
                    messages.append("Invalid username and/or password")

    return render_template('login.html', messages=messages)

@app.route('/logout')
def logout():
    session.pop('username', None)
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

        # VALIDATION CHECKING
        if not username:
            messages.append("Username invalid")
        if not password:
            messages.append("Provide a password")

        # MESSAGES LIST = EMPTY, ZERO ERRORS
        if not messages:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            messages.append("User created successfully")

    return render_template('signup.html', messages=messages)


##############################
#                            #
#           INDEX            #
#                            #
##############################
@app.route('/')
def index():
    #if 'username' in session:
    #    with sqlite3.connect('database.db') as conn:
    #        cursor = conn.cursor()
    #        cursor.execute("SELECT username FROM users WHERE username = ?", (session['username'],))
    #        user = cursor.fetchone()
    #        if user:
    #            return render_template('index.html', username=session['username'])
    #        else:
    #            return redirect(url_for('logout'))
    #else:
    #    return redirect(url_for('login'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
