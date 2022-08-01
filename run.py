from flask import Flask, render_template, g
import sqlite3
app = Flask(__name__)

MENUDB = 'menu.db'



drinks = [
['cola', '$1.00'],
['Vodka', '7.00'],
['Special Vodka' '$705'],
['Water' '2.00']
]

sides = [
['Fries', '$2.00'],
['Onion Rings', '2.50'],
['Mushrooms' '$3.50'],
['Nothing' '$5.00']
]


@app.route('/')
def index():
    db = sqlite3.connect(MENUDB)
    print(db)

burgers = []
cur = db.execute('SELECT burger,price FROM burgers')
    for row in cur:
        burgers.append(list(row))
    db.close()

    return render_template('index.html', disclaimer='may contain nuts',
    burgers=burgers,
    drinks=drinks,
    sides=sides)

@app.route('/order')
def order():
    return render_template('order.html')
