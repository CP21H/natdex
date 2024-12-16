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
#           INDEX            #
#                            #
##############################
@app.route('/')
def index():
    if 'username' in session:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE username = ?", (session['username'],))
            user = cursor.fetchone()
            if user:
                return render_template('index.html', username=session['username'])
            else:
                return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
