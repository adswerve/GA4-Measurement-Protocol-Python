class Event(dict):
    def __init__(self, name):
        self.set_event_name(name)

    def set_event_name(self, name):
        if len(name) > 40:
            raise ValueError("Event name cannot exceed 40 characters.")
        self["event_name"] = name

    def get_event_name(self):
        return self.get("event_name")

    def set_event_param(self, name, value):
        # Series of checks to comply with GA4 event collection limits: https://support.google.com/analytics/answer/9267744
        if len(name) > 40:
            raise ValueError("Event parameter name cannot exceed 40 characters.")
        if len(value) > 100:
            raise ValueError("Event parameter value cannot exceed 100 characters.")
        if "params" not in self.keys():
            self["params"] = {}
        if len(self["params"]) >= 25:
            raise RuntimeError("Event cannot contain more than 25 parameters.")
        self["params"][name] = value

    def get_event_params(self):
        return self.get("params")
        
    def add_item(self, item):
        if not isinstance(item, dict):
            raise ValueError("'item' must be an instance of a dictionary.")
        if "items" not in self["params"].keys():
            self.set_event_param("items", [])
        self["params"]["items"].append(item)