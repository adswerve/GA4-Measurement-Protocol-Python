import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseStore(dict):
    def __init__(self):
        self = {
            "user_properties": {},
            "session_parameters": {}
        }

    def load(self):
        raise NotImplementedError("Subclass should be using this function, but it was called through the base class instead.")

    def save(self):
        raise NotImplementedError("Subclass should be using this function, but it was called through the base class instead.")

    def _check_exists(self, key):
        # Helper function to make sure a key exists before trying to work with values within it.
        if key not in self.keys():
            self[key] = {}

    def _set(self, type, name, value):
        # Helper function to set a single parameter (user or session).
        self._check_exists(type)
        self[type][name] = value

    def _get_one(self, type, name):
        # Helper function to get a single parameter value (user or session).
        self._check_exists(type)
        return self[type].get(name, None)

    def _get_all(self, type=None):
        # Helper function to get all user or session parameters - or the entire dictionary if not specified.
        if type is not None:
            return self[type]
        else:
            return self

    # While redundant, the following make sure the distinction between session and user items is easier for the end user.
    def set_user_property(self, name, value):
        self._set("user_properties", name, value)

    def get_user_property(self, name):
        self.get_one("user_properties", name)

    def get_all_user_properties(self):
        self._get_all("user_properties")

    def set_session_parameter(self, name, value):
        self._set("session_parameters", name, value)

    def get_session_parameter(self, name):
        self.get_one("session_parameters", name)

    def get_all_session_parameters(self):
        self._get_all("session_parameters")

class DictStore(BaseStore):
    def __init__(self):
        super().__init__()

    def load(self, data):
        assert isinstance(data, dict), "loaded data must inherit from dict"
        self = data

    def save(self):
        # Give the user back what's in the dictionary so they can decide how to save it.
        self._get_all()

class FileStore(BaseStore):
    def __init__(self, data_location):
        super().__init__()
        try:
            self.load(data_location)
        except:
            logger.info(f"Failed to find file at location: {data_location}")

    def load(self, data_location):
        # Function to get data from the specified data location, then make sure the FileStore knows where the data is expected.
        with open(data_location, "r") as json_file:
            self = json.load(json_file)
        self["data_location"] = data_location

    def save(self, data_location=None):
        # Function to save the current dictionary to a JSON file at the specified location.
        try:
            save_location = data_location or self["data_location"]
            self["data_location"] = save_location
            with open(save_location, "w") as outfile:
                json.dump(self, outfile)
        except:
            logger.info(f"Failed to save file at location: {save_location}")