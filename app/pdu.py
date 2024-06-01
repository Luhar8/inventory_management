import struct

MSG_TYPE_QUERY_INVENTORY = 1
MSG_TYPE_INVENTORY_RESPONSE = 2
MSG_TYPE_UPDATE_INVENTORY = 3

class QueryInventoryMessage:
    def __init__(self, client_id, timestamp):
        self.message_type = MSG_TYPE_QUERY_INVENTORY
        self.client_id = client_id
        self.timestamp = timestamp

    def to_bytes(self):
        return struct.pack('!B I Q', self.message_type, self.client_id, self.timestamp)

    @staticmethod
    def from_bytes(data):
        message_type, client_id, timestamp = struct.unpack('!B I Q', data)
        return QueryInventoryMessage(client_id, timestamp)

class InventoryResponseMessage:
    def __init__(self, item_id, item_name, quantity):
        self.message_type = MSG_TYPE_INVENTORY_RESPONSE
        self.item_id = item_id
        self.item_name = item_name
        self.quantity = quantity

    def to_bytes(self):
        item_name_encoded = self.item_name.encode('utf-8')
        return struct.pack(f'!B I I {len(item_name_encoded)}s', self.message_type, self.item_id, self.quantity, item_name_encoded)

    @staticmethod
    def from_bytes(data):
        message_type, item_id, quantity = struct.unpack('!B I I', data[:9])
        item_name = data[9:].decode('utf-8')
        return InventoryResponseMessage(item_id, item_name, quantity)

class UpdateInventoryMessage:
    def __init__(self, item_id, quantity_change):
        self.message_type = MSG_TYPE_UPDATE_INVENTORY
        self.item_id = item_id
        self.quantity_change = quantity_change

    def to_bytes(self):
        return struct.pack('!B I i', self.message_type, self.item_id, self.quantity_change)

    @staticmethod
    def from_bytes(data):
        message_type, item_id, quantity_change = struct.unpack('!B I i', data)
        return UpdateInventoryMessage(item_id, quantity_change)
