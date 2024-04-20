from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to connect to the database
def connect_db():
    return sqlite3.connect("test.db")

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, barcode, price FROM example")
    items = cursor.fetchall()
    connection.close()
    return render_template('market.html', items=items)

# Route to handle form submission for adding a new item
@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.form['name']
        barcode = request.form['barcode']
        price = request.form['price']

        # Connect to the database
        connection = connect_db()
        cursor = connection.cursor()

        # Insert the new item into the database
        cursor.execute("INSERT INTO example (name, barcode, price) VALUES (?, ?, ?)", (name, barcode, price))

        # Commit the transaction and close the connection
        connection.commit()
        connection.close()

        # Redirect to the market page
        return redirect(url_for('market_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
