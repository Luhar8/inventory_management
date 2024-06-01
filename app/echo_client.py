from typing import Dict
from app.echo_quic import EchoQuicConnection, QuicStreamEvent
from app.pdu import QueryInventoryMessage, InventoryResponseMessage, UpdateInventoryMessage

async def fetch_inventory(conn: EchoQuicConnection):
    # Create a Query Inventory Message (QIM)
    qim = pdu.QueryInventoryMessage(client_id=12345, timestamp=1622547800)
    
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

async def update_inventory_item(conn: EchoQuicConnection, item_id, quantity_change):
    # Create an Update Inventory Message (UIM)
    uim = pdu.UpdateInventoryMessage(item_id=item_id, quantity_change=quantity_change)
    
    new_stream_id = conn.new_stream()
    qs = QuicStreamEvent(new_stream_id, uim.to_bytes(), False)
    await conn.send(qs)
    
    # Receive updated Inventory Response Message (IRM)
    message: QuicStreamEvent = await conn.receive()
    irm = pdu.InventoryResponseMessage.from_bytes(message.data)
    
    return {"id": irm.item_id, "name": irm.item_name, "quantity": irm.quantity}
