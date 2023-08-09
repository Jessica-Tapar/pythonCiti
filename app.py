from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from datetime import datetime


import stock_data

app = Flask(__name__)
app.secret_key = 'Jessica@123'  # Replace with your secret key

# Replace with your MySQL credentials
db_config = {
    'user': 'root',
    'password': 'Jessica@123',
    'database': 'restapi'
}

data = stock_data.collect_data()


@app.route('/')
def home():
    if 'username' in session:
        return render_template('saved_stocks.html', data=data)
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    invalid_login = False

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        query = "SELECT * FROM login WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))

        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            session['username'] = user[1]
            return redirect('/')
        else:
            invalid_login = True

    return render_template('login.html', invalid_login=invalid_login)


@app.route('/', methods=['POST'])
def save_stock():
    saved = request.json
    company_name = saved['company']
    nse_value = float(saved['nse'])
    bse_value = float(saved['bse'])
    suggest_buy = saved['suggestBuy']
    suggest_sell = saved['suggestSell']
    arbitrage = float(saved['arbitrage'])
    date_string = saved['date']  # Assuming this is a date string in your format
    input_date_format = '%Y-%m-%d'  # Adjust this format according to your saved['date'] format

    # Convert the date string to a Python datetime object
    date_object = datetime.strptime(date_string, input_date_format)

    # Convert the Python datetime object to a MySQL-compatible date string
    date = date_object.strftime('%Y-%m-%d')

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        insert_query = (
            "INSERT INTO saved_stocks (Company, NSE, BSE, SuggestedBuy, SuggestedSell, Arbitrage, Date)"
            "VALUES (%s, %s, %s, %s, %s, %s,%s)"
        )

        values = (company_name, nse_value, bse_value, suggest_buy, suggest_sell, arbitrage, date)
        cursor.execute(insert_query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Row saved successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/saved_stocks')
def display_table():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    query = "SELECT * FROM saved_stocks"  # Replace with your table name
    cursor.execute(query)

    table_data = cursor.fetchall()

    cursor.close()
    connection.close()

    print(table_data)
    return render_template('saved.html', table_data=table_data)

# ... Your existing routes ...
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
