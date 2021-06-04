import json


class APIAutomation:
    def __init__(self, random, random_float, bool1, date, firstname, lastname, city, email_uses_current_data,
                 array, Array_Of_Obj):
        self.random = random
        self.random_float = random_float
        self.bool = bool1
        self.date = date
        self.firstname = firstname
        self.lastname = lastname
        self.city = city
        self.email_uses_current_data = email_uses_current_data
        self.array = array
        self.key = Array_Of_Obj[0]
        self.value = Array_Of_Obj[1]


with open('resultJSON.txt') as f:
    json_data = json.load(f)
    print(json_data)
    object1 = APIAutomation(**json_data)
    print("From json to class")
    print(object1.random, object1.random_float, object1.bool, object1.date, object1.firstname, object1.lastname,
          object1.email_uses_current_data, object1.city, object1.array, object1.key, object1.value)

    string_json = json.dumps(object1.__dict__)
    print(" Object to string :")
    print(string_json)
