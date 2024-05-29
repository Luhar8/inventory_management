# inventory = {
#     1: {"id": 1, "name": "Apple", "quantity": 10},
#     2: {"id": 2, "name": "Coffee Bottles", "quantity": 4},
#     3: {"id": 3, "name": "Bread Packet", "quantity": 8},
#     4: {"id": 4, "name": "Potato Bag", "quantity": 3},
#     5: {"id": 5, "name": "Oranges", "quantity": 15},
# }

# def get_inventory():
#     return list(inventory.values())

# def update_inventory(item_id, quantity):
#     if item_id in inventory:
#         inventory[item_id]['quantity'] = quantity
#         return inventory[item_id]
#     return None

inventory = {
    "Apple": 10,
    "Coffee Bottles": 4,
    "Bread Packet": 8,
    "Potato Bag": 3,
    "Oranges": 15,
}

def update_inventory(item_name, action):
    if item_name in inventory:
        if action == "increase":
            inventory[item_name] += 1
        elif action == "decrease" and inventory[item_name] > 0:
            inventory[item_name] -= 1

def get_inventory():
    return inventory
