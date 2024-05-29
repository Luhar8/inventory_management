# import asyncio
# import json
# from aioquic.asyncio import connect
# from aioquic.asyncio.protocol import QuicConnectionProtocol
# from pdu import Datagram, UpdateInventoryMessage
# from quic_engine import build_client_quic_config
# from echo_quic import QuicStreamEvent, EchoQuicConnection

# class InventoryClientProtocol(QuicConnectionProtocol):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.response = None

#     async def update_inventory(self, item_id, quantity, fetch=False):
#         if fetch:
#             pdu = Datagram(0, 0, 0, 0)
#         else:
#             pdu = UpdateInventoryMessage(0, item_id, quantity, 0)

#         pdu_bytes = pdu.to_bytes()

#         stream_id = self._quic.get_next_available_stream_id()
#         event = QuicStreamEvent(stream_id, pdu_bytes, end_stream=True)
        
#         connection = EchoQuicConnection(
#             send=self.send_event(event),
#             receive=self.receive_event(),
#             close=self._quic.close,
#             new_stream=self._quic.get_next_available_stream_id
#         )
        
#         await connection.send(event)
#         response_event = await connection.receive()
        
#         response_pdu = Datagram.from_bytes(response_event.data)
#         print("[client] Received response: ", response_pdu.msg)
        
#         if fetch:
#             self.response = json.loads(response_pdu.msg)
#         else:
#             self.response = response_pdu

#     async def send_event(self, event):
#         await self._quic.send_stream_data(event.stream_id, event.data, event.end_stream)

#     async def receive_event(self):
#         stream_id, data, end_stream = await self._quic.wait_for_event()
#         return QuicStreamEvent(stream_id, data, end_stream)

# async def update_inventory_via_quic(server_address, server_port, cert_file, item_id, quantity, fetch=False):
#     config = build_client_quic_config(cert_file)

#     async with connect(
#         server_address,
#         server_port,
#         configuration=config,
#         create_protocol=InventoryClientProtocol
#     ) as protocol:
       
#         await protocol.update_inventory(item_id, quantity, fetch)
#         return protocol.response




# import asyncio
# from aioquic.asyncio import connect
# from aioquic.quic.configuration import QuicConfiguration
# from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
# from .pdu import Datagram, UpdateInventoryMessage
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# async def send_inventory_update(item_name, action):
#     configuration = QuicConfiguration(is_client=True)
#     configuration.load_verify_locations("certs/quic_certificate.pem")

#     async with connect("localhost", 4433, configuration=configuration) as protocol:
#         await protocol.wait_connected()

#         message = UpdateInventoryMessage(item_name=item_name, action=action)
#         dgram = Datagram(mtype=0x01, msg=message.to_bytes())
#         protocol._quic.send_stream_data(0, dgram.to_bytes())
#         await protocol._quic.send_stream_data(0, b'', end_stream=True)

#         event = await protocol._event_waiter
#         if isinstance(event, StreamDataReceived):
#             response = Datagram.from_bytes(event.data)
#             logger.info(f"Received: {response.msg}")
#             return response.msg
#         return None

# def update_inventory_via_quic(item_name, action):
#     return asyncio.run(send_inventory_update(item_name, action))

import asyncio
from aioquic.asyncio import connect
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import HandshakeCompleted, StreamDataReceived
from .pdu import Datagram, UpdateInventoryMessage, InventoryRequestMessage, InventoryResponseMessage, MSG_TYPE_DATA, MSG_TYPE_DATA_ACK, MSG_TYPE_INVENTORY_REQUEST, MSG_TYPE_INVENTORY_RESPONSE

async def fetch_inventory():
    configuration = QuicConfiguration(is_client=True)
    configuration.load_verify_locations("certs/quic_certificate.pem")

    async with connect("localhost", 4433, configuration=configuration) as protocol:
        await protocol.wait_connected()

        request_message = InventoryRequestMessage()
        dgram = Datagram(mtype=MSG_TYPE_INVENTORY_REQUEST, item_id=0, quantity=0, timestamp=0, msg=request_message.to_bytes())
        protocol._quic.send_stream_data(0, dgram.to_bytes())
        await protocol._quic.send_stream_data(0, b'', end_stream=True)

        event = await protocol._event_waiter
        if isinstance(event, StreamDataReceived):
            response = Datagram.from_bytes(event.data)
            if response.mtype == MSG_TYPE_INVENTORY_RESPONSE:
                inventory_response = InventoryResponseMessage.from_bytes(response.msg)
                return inventory_response.inventory
        return None

async def send_inventory_update(item_name, action):
    configuration = QuicConfiguration(is_client=True)
    configuration.load_verify_locations("certs/quic_certificate.pem")

    async with connect("localhost", 4433, configuration=configuration) as protocol:
        await protocol.wait_connected()

        # Mapping of item names to IDs
        item_mapping = {
            "Apple": 1,
            "Coffee Bottles": 2,
            "Bread Packet": 3,
            "Potato Bag": 4,
            "Oranges": 5
        }

        if item_name in item_mapping:
            item_id = item_mapping[item_name]
            quantity = 1 if action == "increase" else -1
            message = UpdateInventoryMessage(client_id=12345, item_id=item_id, quantity=quantity, timestamp=0)  # Assuming client_id and timestamp
            dgram = Datagram(mtype=MSG_TYPE_DATA, item_id=item_id, quantity=quantity, timestamp=0, msg=message.to_bytes())
            protocol._quic.send_stream_data(0, dgram.to_bytes())
            await protocol._quic.send_stream_data(0, b'', end_stream=True)

            event = await protocol._event_waiter
            if isinstance(event, StreamDataReceived):
                response = Datagram.from_bytes(event.data)
                if response.mtype == MSG_TYPE_DATA_ACK:
                    return True
    return False

def update_inventory_via_quic(item_name, action):
    return asyncio.run(send_inventory_update(item_name, action))

def get_inventory_from_server():
    return asyncio.run(fetch_inventory())

