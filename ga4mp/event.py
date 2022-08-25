class Event(dict):
    def set_event_name(self, name):
        self["event_name"] = name

    def get_event_name(self):
        return self.get("event_name")

    def set_event_param(self, name, value):
        self["params"][name] = value