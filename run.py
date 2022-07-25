from flask import Flask, render_template
app = Flask(__name__)

burgers = [
['Classic Burger', '$5.99'],
['Cheese Burger', '$7.99'],
['Classic Cheesier Burger', '$4.99'],
['Double Burger', '$5.99']
]

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
    return render_template('index.html', disclaimer='may contain nuts',
    burgers=burgers,
    drinks=drinks,
    sides=sides)

@app.route('/order')
def order():
    return render_template('order.html')
