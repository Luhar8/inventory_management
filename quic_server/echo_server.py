# import asyncio
# from typing import Coroutine, Dict
# from echo_quic import EchoQuicConnection, QuicStreamEvent
# from pdu import Datagram, UpdateInventoryMessage
# import server_storage
# import json

# async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
#     message: QuicStreamEvent = await conn.receive()
#     dgram_in = Datagram.from_bytes(message.data)
    
#     if isinstance(dgram_in, UpdateInventoryMessage):
#         item_id = dgram_in.item_id
#         new_quantity = dgram_in.quantity

#         updated_item = server_storage.update_inventory(item_id, new_quantity)
#         if updated_item:
#             print(f"Updated inventory: {updated_item}")

#         stream_id = message.stream_id
#         dgram_out = Datagram(dgram_in.mtype | MSG_TYPE_DATA_ACK, item_id, new_quantity, dgram_in.timestamp)
#         dgram_out.msg = f"SVR-ACK: Updated {updated_item['name']} to {new_quantity}"
#         rsp_msg = dgram_out.to_bytes()
#         rsp_evnt = QuicStreamEvent(stream_id, rsp_msg, False)
#         await conn.send(rsp_evnt)
#     else:
#         # Fetch inventory request
#         inventory_list = server_storage.get_inventory()
#         inventory_data = json.dumps(inventory_list).encode('utf-8')

#         stream_id = message.stream_id
#         dgram_out = Datagram(MSG_TYPE_DATA, 0, 0, 0)
#         dgram_out.msg = inventory_data
#         rsp_msg = dgram_out.to_bytes()
#         rsp_evnt = QuicStreamEvent(stream_id, rsp_msg, False)
#         await conn.send(rsp_evnt)

# async def run_server(listen_address: str, listen_port: int, config):
#     server = await asyncio.start_server(lambda: EchoQuicConnection(echo_server_proto), listen_address, listen_port)
#     async with server:
#         await server.serve_forever()

# import asyncio
# from typing import Dict
# from .echo_quic import EchoQuicConnection, QuicStreamEvent
# from .pdu import Datagram, MSG_TYPE_DATA_ACK, UpdateInventoryMessage
# from .server_storage import update_inventory

# async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
#     message: QuicStreamEvent = await conn.receive()

#     dgram_in = Datagram.from_bytes(message.data)
#     msg = UpdateInventoryMessage.from_bytes(dgram_in.msg)

#     update_inventory(msg.item_name, msg.action)

#     dgram_out = dgram_in
#     dgram_out.mtype |= MSG_TYPE_DATA_ACK
#     dgram_out.msg = f"SVR-ACK: {msg.item_name} {msg.action}"
#     rsp_msg = dgram_out.to_bytes()
#     rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
#     await conn.send(rsp_evnt)

# def main():
#     import argparse
#     from aioquic.asyncio import serve
#     from .quic_engine import build_server_quic_config

#     parser = argparse.ArgumentParser(description="QUIC Echo Server")
#     parser.add_argument("--cert-file", type=str, required=True)
#     parser.add_argument("--key-file", type=str, required=True)
#     parser.add_argument("--host", type=str, default="localhost")
#     parser.add_argument("--port", type=int, default=4433)
#     args = parser.parse_args()

#     configuration = build_server_quic_config(args.cert_file, args.key_file)

#     loop = asyncio.get_event_loop()
#     server = loop.run_until_complete(
#         serve(
#             args.host,
#             args.port,
#             configuration=configuration,
#             create_protocol=echo_server_proto
#         )
#     )

#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass

# if __name__ == "__main__":
#     main()


# import asyncio
# from typing import Coroutine, Dict
# import json
# from echo_quic import EchoQuicConnection, QuicStreamEvent
# from pdu import Datagram, UpdateInventoryMessage, InventoryRequestMessage, InventoryResponseMessage, MSG_TYPE_DATA_ACK, MSG_TYPE_INVENTORY_REQUEST, MSG_TYPE_INVENTORY_RESPONSE

# inventory_data = {
#     1: {"name": "Apple", "quantity": 10},
#     2: {"name": "Coffee Bottles", "quantity": 4},
#     3: {"name": "Bread Packet", "quantity": 8},
#     4: {"name": "Potato Bag", "quantity": 3},
#     5: {"name": "Oranges", "quantity": 15},
# }

# def get_inventory():
#     return inventory_data

# def update_inventory(item_id, quantity, action):
#     if item_id in inventory_data:
#         if action == "increase":
#             inventory_data[item_id]["quantity"] += quantity
#         elif action == "decrease":
#             inventory_data[item_id]["quantity"] = max(0, inventory_data[item_id]["quantity"] - quantity)

# async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
#     message: QuicStreamEvent = await conn.receive()
#     dgram_in = Datagram.from_bytes(message.data)
    
#     if dgram_in.mtype == MSG_TYPE_INVENTORY_REQUEST:
#         inventory = get_inventory()
#         response_message = InventoryResponseMessage(inventory)
#         dgram_out = Datagram(mtype=MSG_TYPE_INVENTORY_RESPONSE, item_id=0, quantity=0, timestamp=0, msg=response_message.to_bytes())
#     elif dgram_in.mtype == MSG_TYPE_DATA:
#         msg = UpdateInventoryMessage.from_bytes(dgram_in.msg)
#         update_inventory(msg.item_id, msg.quantity, msg.msg)  # Assuming msg contains the action
#         dgram_out = Datagram(mtype=MSG_TYPE_DATA_ACK, item_id=msg.item_id, quantity=msg.quantity, timestamp=0, msg=f"SVR-ACK: {msg.item_id} {msg.msg}")
    
#     rsp_msg = dgram_out.to_bytes()
#     rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
#     await conn.send(rsp_evnt)

# def main():
#     # Existing main function code

import asyncio
from typing import Coroutine, Dict
from aioquic.asyncio.protocol import QuicConnectionProtocol, QuicStreamHandler
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration
from .echo_quic import EchoQuicConnection, QuicStreamEvent
from .pdu import Datagram, UpdateInventoryMessage, InventoryRequestMessage, InventoryResponseMessage, MSG_TYPE_DATA_ACK, MSG_TYPE_INVENTORY_REQUEST, MSG_TYPE_INVENTORY_RESPONSE

inventory_data = {
    1: {"name": "Apple", "quantity": 10},
    2: {"name": "Coffee Bottles", "quantity": 4},
    3: {"name": "Bread Packet", "quantity": 8},
    4: {"name": "Potato Bag", "quantity": 3},
    5: {"name": "Oranges", "quantity": 15},
}

def get_inventory():
    return inventory_data

def update_inventory(item_id, quantity, action):
    if item_id in inventory_data:
        if action == "increase":
            inventory_data[item_id]["quantity"] += quantity
        elif action == "decrease":
            inventory_data[item_id]["quantity"] = max(0, inventory_data[item_id]["quantity"] - quantity)

async def echo_server_proto(scope: Dict, conn: EchoQuicConnection):
    message: QuicStreamEvent = await conn.receive()
    dgram_in = Datagram.from_bytes(message.data)
    
    if dgram_in.mtype == MSG_TYPE_INVENTORY_REQUEST:
        inventory = get_inventory()
        response_message = InventoryResponseMessage(inventory)
        dgram_out = Datagram(mtype=MSG_TYPE_INVENTORY_RESPONSE, item_id=0, quantity=0, timestamp=0, msg=response_message.to_bytes())
    elif dgram_in.mtype == MSG_TYPE_DATA:
        msg = UpdateInventoryMessage.from_bytes(dgram_in.msg)
        update_inventory(msg.item_id, msg.quantity, msg.msg)  # Assuming msg contains the action
        dgram_out = Datagram(mtype=MSG_TYPE_DATA_ACK, item_id=msg.item_id, quantity=msg.quantity, timestamp=0, msg=f"SVR-ACK: {msg.item_id} {msg.msg}")
    
    rsp_msg = dgram_out.to_bytes()
    rsp_evnt = QuicStreamEvent(message.stream_id, rsp_msg, False)
    await conn.send(rsp_evnt)

class EchoQuicServerProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = EchoQuicConnection(
            send=self._send_data,
            receive=self._receive_data(),
            close=self._close_stream,
            new_stream=self._create_stream
        )

    async def _send_data(self, event: QuicStreamEvent):
        self._quic.send_stream_data(event.stream_id, event.data, end_stream=event.end_stream)
    
    async def _receive_data(self):
        while True:
            event = await self._quic._events.get()
            if isinstance(event, StreamDataReceived):
                yield QuicStreamEvent(stream_id=event.stream_id, data=event.data, end_stream=event.end_stream)
    
    def _close_stream(self):
        self._quic.send_connection_close(0, b'')
    
    def _create_stream(self):
        return self._quic.get_next_available_stream_id()

async def main():
    configuration = QuicConfiguration(is_client=False)
    configuration.load_cert_chain(certfile='certs/quic_certificate.pem', keyfile='certs/quic_private_key.pem')
    
    await serve(
        "localhost",
        4433,
        configuration=configuration,
        create_protocol=EchoQuicServerProtocol
    )

if __name__ == '__main__':
    asyncio.run(main())

