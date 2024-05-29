# import struct

# MSG_TYPE_DATA = 0x00
# MSG_TYPE_DATA_ACK = 0x01

# class Datagram:
#     def __init__(self, mtype, item_id, quantity, timestamp, msg=""):
#         self.mtype = mtype
#         self.item_id = item_id
#         self.quantity = quantity
#         self.timestamp = timestamp
#         self.msg = msg

#     def to_bytes(self):
#         msg_bytes = self.msg.encode('utf-8')
#         msg_length = len(msg_bytes)
#         return struct.pack(f'!B I Q {msg_length}s', self.mtype, self.item_id, self.quantity, msg_bytes)

#     @staticmethod
#     def from_bytes(data):
#         mtype, item_id, quantity = struct.unpack('!B I Q', data[:13])
#         msg = data[13:].decode('utf-8')
#         return Datagram(mtype, item_id, quantity, 0, msg)

# class UpdateInventoryMessage(Datagram):
#     def __init__(self, client_id, item_id, quantity, timestamp):
#         super().__init__(MSG_TYPE_DATA, item_id, quantity, timestamp)
#         self.client_id = client_id

#     def to_bytes(self):
#         msg_bytes = self.msg.encode('utf-8')
#         msg_length = len(msg_bytes)
#         return struct.pack(f'!B I Q Q {msg_length}s', self.mtype, self.item_id, self.quantity, self.client_id, msg_bytes)

#     @staticmethod
#     def from_bytes(data):
#         mtype, item_id, quantity, client_id = struct.unpack('!B I Q Q', data[:21])
#         msg = data[21:].decode('utf-8')
#         return UpdateInventoryMessage(client_id, item_id, quantity, 0)


# import struct

# class Datagram:
#     def __init__(self, mtype: int, msg: bytes):
#         self.mtype = mtype
#         self.msg = msg

#     def to_bytes(self):
#         mtype_bytes = struct.pack("!B", self.mtype)
#         msg_len = struct.pack("!I", len(self.msg))
#         return mtype_bytes + msg_len + self.msg

#     @staticmethod
#     def from_bytes(data: bytes):
#         mtype = struct.unpack("!B", data[0:1])[0]
#         msg_len = struct.unpack("!I", data[1:5])[0]
#         msg = data[5:5+msg_len]
#         return Datagram(mtype, msg)

# MSG_TYPE_DATA_ACK = 0x01

# class UpdateInventoryMessage:
#     def __init__(self, item_name: str, action: str):
#         self.item_name = item_name
#         self.action = action

#     def to_bytes(self):
#         item_name_bytes = self.item_name.encode("utf-8")
#         action_bytes = self.action.encode("utf-8")
#         return struct.pack("!B", len(item_name_bytes)) + item_name_bytes + action_bytes

#     @staticmethod
#     def from_bytes(data: bytes):
#         item_name_len = struct.unpack("!B", data[0:1])[0]
#         item_name = data[1:1+item_name_len].decode("utf-8")
#         action = data[1+item_name_len:].decode("utf-8")
#         return UpdateInventoryMessage(item_name, action)

import struct
import json

MSG_TYPE_DATA = 0x00
MSG_TYPE_DATA_ACK = 0x01
MSG_TYPE_INVENTORY_REQUEST = 0x02
MSG_TYPE_INVENTORY_RESPONSE = 0x03

class Datagram:
    def __init__(self, mtype, item_id, quantity, timestamp, msg=""):
        self.mtype = mtype
        self.item_id = item_id
        self.quantity = quantity
        self.timestamp = timestamp
        self.msg = msg

    def to_bytes(self):
        msg_bytes = self.msg.encode('utf-8')
        msg_length = len(msg_bytes)
        return struct.pack(f'!B I Q {msg_length}s', self.mtype, self.item_id, self.quantity, msg_bytes)

    @staticmethod
    def from_bytes(data):
        mtype, item_id, quantity = struct.unpack('!B I Q', data[:13])
        msg = data[13:].decode('utf-8')
        return Datagram(mtype, item_id, quantity, 0, msg)

class UpdateInventoryMessage(Datagram):
    def __init__(self, client_id, item_id, quantity, timestamp):
        super().__init__(MSG_TYPE_DATA, item_id, quantity, timestamp)
        self.client_id = client_id

    def to_bytes(self):
        msg_bytes = self.msg.encode('utf-8')
        msg_length = len(msg_bytes)
        return struct.pack(f'!B I Q Q {msg_length}s', self.mtype, self.item_id, self.quantity, self.client_id, msg_bytes)

    @staticmethod
    def from_bytes(data):
        mtype, item_id, quantity, client_id = struct.unpack('!B I Q Q', data[:21])
        msg = data[21:].decode('utf-8')
        return UpdateInventoryMessage(client_id, item_id, quantity, 0)

class InventoryRequestMessage:
    def to_bytes(self):
        return b''  # No additional data needed for inventory request

class InventoryResponseMessage:
    def __init__(self, inventory):
        self.inventory = inventory

    def to_bytes(self):
        inventory_bytes = json.dumps(self.inventory).encode('utf-8')
        return struct.pack("!I", len(inventory_bytes)) + inventory_bytes

    @staticmethod
    def from_bytes(data):
        inventory_len = struct.unpack("!I", data[0:4])[0]
        inventory = json.loads(data[4:4+inventory_len].decode('utf-8'))
        return InventoryResponseMessage(inventory)
