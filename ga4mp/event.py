class Event(dict):
    def __init__(self, name):
        self.set_event_name(name)
        
    def set_event_name(self, name):
        self["event_name"] = name

    def get_event_name(self):
        return self.get("event_name")

    def set_event_param(self, name, value): # TODO: add validation functions for bad event names or parameters, etc.
        if "params" not in self.keys():
            self["params"] = {}
        self["params"][name] = value