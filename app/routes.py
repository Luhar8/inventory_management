from flask import render_template, request, redirect, url_for
from app import app

# Predefined users for demonstration
users = {
    "admin": "adminpass",
    "user": "userpass"
}

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('inventory'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/inventory')
def inventory():
    # Dummy inventory data
    inventory_items = [
        {"name": "Apple", "quantity": 10},
        {"name": "Coffee Bottles", "quantity": 4},
        {"name": "Bread Packet", "quantity": 8},
        {"name": "Potato Bag", "quantity": 3},
        {"name": "Oranges", "quantity": 15},
    ]
    return render_template('inventory.html', items=inventory_items)
