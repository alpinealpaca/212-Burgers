from flask import Flask, render_template, g, request, session, redirect, url_for
import sqlite3
app = Flask(__name__)
app.secret_key = '123456789'

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



def fetchMenu(con):
    burgers = []
    free = '0'
    cur = con.execute('SELECT burger,price FROM burgers')
    for row in cur:
        burgers.append(list(row))

    drinks = []
    cur = con.execute('SELECT drinks,price FROM drinks')
    for row in cur:
        drinks.append(list(row))

    sides = []
    cur = con.execute('SELECT sides,price FROM sides')
    for row in cur:
        sides.append(list(row))

    return {'burgers':burgers, 'drinks':drinks, 'sides':sides}
    #return render_template('index.html',
    #disclaimer='may contain nuts',
    #burgers=menu['burgers'], #burgers=burgers,
    #drinks=menu['drinks'],#drinks=drinks,
    #sides=menu['sides'] #sides=sides)

@app.route('/')
def index():
    db = sqlite3.connect(MENUDB)
    menu = fetchMenu(db)
    db.close()
    return render_template(
    'index.html',
    disclaimer='may contain traces of nuts',
    burgers=menu['burgers'],
    drinks=menu['drinks'],
    sides=menu['sides']
    )

@app.route('/order')
def order():
    #return render_template('order.html')
    db = sqlite3.connect(MENUDB)
    menu = fetchMenu(db)
    db.close()
    return render_template('order.html', burgers=menu['burgers'], drinks=menu['drinks'], sides=menu['sides'])
    #burgers = []
    #free = '0'
    #cur = con.execute('SELECT burger,price FROM burgers WHERE price>=?', (free,))
    #for row in cur:
    #    burgers.append(list(row))

    #drinks = []
    #cur = con.execute('SELECT drink,price FROM drinks')
    #for row in cur:
#        drinks.append(list(row))

#    sides = []
#    cur = con.execute('SELECT side,price FROM sides')
#    for row in cur:
#        sides.append(list(row))

#    db.close()

    return render_template('order.html', burgers=burgers, drinks=drinks, sides=sides)


@app.route('/confirm', methods=['POST'])
def confirm():

    details = {}
    items = {}

    for input in request.form:
        if input == 'name' or input == 'address':
            details[input] = request.form[input]
        elif request.form[input] and request.form[input] != '0':
            items[input] = request.form[input]

    db = sqlite3.connect(MENUDB)
    cur = db.execute()
    'INSERT INTO orders(name, address, items) VALUES(?, ?, ?)',
    (details['name'], details['address'], str(items))

    con.commit()
    con.close()


    return render_template('confirm.html', details=details, items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username'] == 'admin':
        session['username'] = request.form['username']
        return redirect(url_for('panel'))
    else:
        return render_template('login.html')

@app.route('/panel')
def panel():
    orders = []
    if 'username' in session:
        con = sqlite3.connect(MENUDB)
        cur = con.execute('SELECT * FROM orders')
        for row in cur:
            orders.append(list(row))
        con.close()
        return render_template('panel.html', orders=orders)
    else:
        return render_template('login.html')

@app.route('/vieworder/<order_id>')
def viewOrder(order_id):
    if 'username' in session:
        con = sqlite3.connect(MENUDB)
        cur = con.execute('SELECT * FROM orders WHERE id=?', (order_id,))
        order = cur.fetchone()
        con.close()
        return str(order) + ' user: ' + session['username']
    else:
        return redirect(url_for('login')) #render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('index'))
