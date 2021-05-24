import json
from json import JSONEncoder


class payloadencoder(JSONEncoder):
    def default(self, object):
        return object.__dict__

