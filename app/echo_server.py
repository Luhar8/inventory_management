import asyncio
from typing import Dict
from app.echo_quic import EchoQuicConnection, QuicStreamEvent
import app.pdu

# Simulated inventory database
inventory_db = {
    1: {"item_name": "Apple", "quantity": 10},
    2: {"item_name": "Coffee Bottles", "quantity": 4},
    3: {"item_name": "Bread Packet", "quantity": 8},
    4: {"item_name": "Potato Bag", "quantity": 3},
    5: {"item_name": "Oranges", "quantity": 15},
}

async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
    message: QuicStreamEvent = await conn.receive()
    
    if message.data[0] == pdu.MSG_TYPE_QUERY_INVENTORY:
        dgram_in = pdu.QueryInventoryMessage.from_bytes(message.data)
        print("[svr] received message: ", dgram_in.__dict__)
        
        # Create an Inventory Response Message (IRM)
        items = []
        for item_id, item in inventory_db.items():
            irm = pdu.InventoryResponseMessage(item_id=item_id, item_name=item["item_name"], quantity=item["quantity"])
            items.append(irm.to_bytes())
        
        for item in items:
            rsp_evnt = QuicStreamEvent(message.stream_id, item, False)
            await conn.send(rsp_evnt)
    
    elif message.data[0] == pdu.MSG_TYPE_UPDATE_INVENTORY:
        uim = pdu.UpdateInventoryMessage.from_bytes(message.data)
        print("[svr] received update message: ", uim.__dict__)
        
        # Update the inventory
        if uim.item_id in inventory_db:
            inventory_db[uim.item_id]["quantity"] += uim.quantity_change
        
        # Send updated Inventory Response Message (IRM)
        item = inventory_db[uim.item_id]
        irm = pdu.InventoryResponseMessage(item_id=uim.item_id, item_name=item["item_name"], quantity=item["quantity"])
        rsp_msg = irm.to_bytes()
        rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
        await conn.send(rsp_evnt)
