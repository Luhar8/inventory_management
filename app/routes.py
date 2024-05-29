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

# @app.route('/update_inventory', methods=['POST'])
# def update_inventory():
#     item_id = int(request.form['item_id'])
#     quantity = int(request.form['quantity'])

#     server_address = 'localhost'
#     server_port = 4433
#     cert_file = './certs/quic_certificate.pem'

#     async def update_inventory_async():
#         response = await update_inventory_via_quic(server_address, server_port, cert_file, item_id, quantity)
#         return response

#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     response = loop.run_until_complete(update_inventory_async())

#     if response:
#         return jsonify({
#             "item_id": response.item_id,
#             "item_name": response.item_name,
#             "quantity": response.quantity
#         })
#     else:
#         return jsonify({"error": "Failed to update inventory"}), 500