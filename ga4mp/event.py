class Event(dict):
    def __init__(self, name):
        self.set_event_name(name)

    def set_event_name(self, name):
        if len(name) > 40:
            raise ValueError("Event name cannot exceed 40 characters.")
        self["event_name"] = name

    def get_event_name(self):
        return self.get("event_name")

    def set_event_param(self, name, value): # TODO: add validation functions for bad event names or parameters, etc.
        if "params" not in self.keys():
            self["params"] = {}
        self["params"][name] = value

    def add_item(self, item):
        if not isinstance(item, dict):
            raise ValueError("'item' must be an instance of a dictionary.")
        if "items" not in self["params"].keys():
            self.set_event_param("items", [])
        self["params"]["items"].append(item)