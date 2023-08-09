import mysql.connector
from flask import Flask, render_template, request, redirect, session
import os

# Generate a random secret key
secret_key = os.urandom(24)


app = Flask(__name__)
app.secret_key = secret_key

# Replace with your actual username and password

db_config = {
    'user': 'root',
    'password': 'Jessica@123',
    'database': 'restapi'
}
# username = 'root'
# password = 'Jessica@123'
# database_name = 'restapi'
#
# # Establish the connection
# connection = mysql.connector.connect(
#     user=username,
#     password=password,
#     database=database_name
#
# )

# if db_config.is_connected():
#     print("Connected to MySQL database")


# Create a cursor
@app.route('/')
def index():
    if 'user_id' in session:
        return f"Welcome, User {session['user_id']}"
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')


if __name__ == '__main__':
    app.run()
