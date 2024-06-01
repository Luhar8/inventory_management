from flask import render_template, request, redirect, url_for, jsonify
from app import app, pdu
import asyncio
from .echo_quic import EchoQuicConnection, QuicStreamEvent
import app.quic_engine

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
    # Fetch inventory data from the server
    inventory_items = asyncio.run(fetch_inventory())
    return render_template('inventory.html', items=inventory_items)

@app.route('/update_inventory', methods=['POST'])
def update_inventory():
    data = request.json
    item_id = data['item_id']
    quantity_change = data['quantity']
    
    # Update inventory on the server
    updated_item = asyncio.run(update_inventory_item(item_id, quantity_change))
    
    if updated_item:
        return jsonify({"quantity": updated_item["quantity"]})
    else:
        return jsonify({"error": "Failed to update inventory"}), 500

async def fetch_inventory():
    # Create a Query Inventory Message (QIM)
    qim = app.pdu.QueryInventoryMessage(client_id=12345, timestamp=1622547800)
    
    async with connect_to_server() as conn:
        new_stream_id = conn.new_stream()
        qs = QuicStreamEvent(new_stream_id, qim.to_bytes(), False)
        await conn.send(qs)
        
        # Receive Inventory Response Message (IRM)
        items = []
        while True:
            message: QuicStreamEvent = await conn.receive()
            if not message:
                break
            irm = pdu.InventoryResponseMessage.from_bytes(message.data)
            items.append({"id": irm.item_id, "name": irm.item_name, "quantity": irm.quantity})
        
        return items

async def update_inventory_item(item_id, quantity_change):
    # Create an Update Inventory Message (UIM)
    uim = pdu.UpdateInventoryMessage(item_id=item_id, quantity_change=quantity_change)
    
    async with connect_to_server() as conn:
        new_stream_id = conn.new_stream()
        qs = QuicStreamEvent(new_stream_id, uim.to_bytes(), False)
        await conn.send(qs)
        
        # Receive updated Inventory Response Message (IRM)
        message: QuicStreamEvent = await conn.receive()
        irm = pdu.InventoryResponseMessage.from_bytes(message.data)
        
        return {"id": irm.item_id, "name": irm.item_name, "quantity": irm.quantity}

async def connect_to_server():
    server_address = 'localhost'
    server_port = 4433
    cert_file = './cert/cert.prem'
    
    config = quic_engine.build_client_quic_config(cert_file)
    return await quic_engine.connect(server_address, server_port, config)