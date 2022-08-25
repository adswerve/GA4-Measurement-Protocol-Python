class Item(dict):
    def __init__(self, item_id=None, item_name=None):
        if item_id is None and item_name is None:
            raise ValueError("At least one of 'item_id' and 'item_name' is required.")
        self.set_item_id(item_id)
        self.set_item_name(item_name)

    def set_item_id(self, item_id):
        self["item_id"] = item_id

    def set_item_name(self, item_name):
        self["item_name"] = item_name