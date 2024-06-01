# # from flask import render_template, request, redirect, url_for
# # from app import app
# # import asyncio
# # from quic_server.echo_client import update_inventory_via_quic

# # # Predefined users for demonstration
# # users = {
# #     "admin": "adminpass",
# #     "user": "userpass"
# # }

# # @app.route('/')
# # @app.route('/login', methods=['GET', 'POST'])
# # def login():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         if username in users and users[username] == password:
# #             return redirect(url_for('inventory'))
# #         else:
# #             return render_template('login.html', error="Invalid credentials")
# #     return render_template('login.html')

# # @app.route('/inventory')
# # def inventory():
# #     # Fetch inventory from the server
# #     inventory_items = asyncio.run(fetch_inventory_from_quic_server())
# #     return render_template('inventory.html', items=inventory_items)

# # @app.route('/update_inventory', methods=['POST'])
# # def update_inventory():
# #     item_id = int(request.form['item_id'])
# #     action = request.form['action']

# #     # Fetch the current inventory from the server
# #     inventory_items = asyncio.run(fetch_inventory_from_quic_server())

# #     # Find the item and update its quantity
# #     for item in inventory_items:
# #         if item['id'] == item_id:
# #             if action == 'increment':
# #                 item['quantity'] += 1
# #             elif action == 'decrement' and item['quantity'] > 0:
# #                 item['quantity'] -= 1
# #             # Update the inventory on the server
# #             asyncio.run(update_inventory_on_quic_server(item_id, item['quantity']))
# #             break

# #     return redirect(url_for('inventory'))

# # async def fetch_inventory_from_quic_server():
# #     server_address = 'localhost'
# #     server_port = 4433
# #     cert_file = './certs/quic_certificate.pem'
# #     return await update_inventory_via_quic(server_address, server_port, cert_file, 0, 0, fetch=True)

# # async def update_inventory_on_quic_server(item_id, quantity):
# #     server_address = 'localhost'
# #     server_port = 4433
# #     cert_file = './certs/quic_certificate.pem'
# #     return await update_inventory_via_quic(server_address, server_port, cert_file, item_id, quantity)

# from flask import render_template, request, redirect, url_for
# from app import app
# from quic_server.echo_client import update_inventory_via_quic
# from quic_server.echo_server import get_inventory

# # Predefined users for demonstration
# users = {
#     "admin": "adminpass",
#     "user": "userpass"
# }

# @app.route('/')
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             return redirect(url_for('inventory'))
#         else:
#             return render_template('login.html', error="Invalid credentials")
#     return render_template('login.html')

# # @app.route('/inventory', methods=['GET', 'POST'])
# # def inventory():
# #     if request.method == 'POST':
# #         item_name = request.form['item_name']
# #         action = request.form['action']
# #         result = update_inventory_via_quic(item_name, action)
# #         if not result:
# #             return render_template('inventory.html', error="Failed to update inventory")
    
# #     # Fetch updated inventory from the server
# #     inventory_items = get_inventory_from_server()
# #     return render_template('inventory.html', items=inventory_items)

# # def get_inventory_from_server():
# #     # This function should implement the logic to fetch inventory from the QUIC server
# #     return []
# @app.route('/inventory', methods=['GET', 'POST'])
# def inventory():
#     if request.method == 'POST':
#         item_name = request.form['item_name']
#         action = request.form['action']
#         result = update_inventory_via_quic(item_name, action)
#         if not result:
#             return render_template('inventory.html', error="Failed to update inventory")
    
#     # Fetch updated inventory from the server
#     inventory_items = get_inventory()
#     return render_template('inventory.html', items=inventory_items)

from flask import render_template, request, redirect, url_for
from app import app
from quic_server.echo_client import update_inventory_via_quic
from quic_server.echo_server import get_inventory

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

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    if request.method == 'POST':
        item_id = int(request.form['item_id'])
        action = request.form['action']
        result = update_inventory_via_quic(item_id, action)
        if not result:
            return render_template('inventory.html', items=get_inventory(), error="Failed to update inventory")
    
    # Fetch updated inventory from the server
    inventory_items = get_inventory()
    print(inventory_items)
    return render_template('inventory.html', items=inventory_items)
