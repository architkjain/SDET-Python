import json
from collections import namedtuple
file_obj_r = open("testdata6json.txt", 'r')
data1 = file_obj_r.read()


# Assignment 6
def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

# Parse JSON into an object with attributes corresponding to dict keys.


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


x = json2obj(data1)
print(x)

# Assignment 7
Json_str = json.dumps(x)
print(Json_str)
