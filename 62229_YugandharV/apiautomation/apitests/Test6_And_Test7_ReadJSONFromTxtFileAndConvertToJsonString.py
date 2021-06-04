import requests
import unittest
import json


class APITest:
    def __init__(self, random, randomfloat, bool, date, firstname, lastname, city, emailusescurrentdata, array,
                 ArrayOfObj, ):
        self.random = random
        self.randomfloat = randomfloat
        self.bool = bool
        self.date = date
        self.firstname = firstname
        self.lastname = lastname
        self.city = city
        self.emailusescurrentdata = emailusescurrentdata
        self.array = array
        self.index = ArrayOfObj[0]
        self.val = ArrayOfObj[1]


file = open("E:\\SDET_Test_Assessment\\apiautomation\\apitests\\JSon.txt", "r")
jsonFile = file.read()
jsonresponse = json.loads(jsonFile)
print(jsonresponse)
class_object = APITest(**jsonresponse)
print("========= PRINTING VALUES FROM CLASS OBJECT===========")
print(class_object.random)
print(class_object.randomfloat)
print(class_object.bool)
print(class_object.date)
print(class_object.firstname)
print(class_object.lastname)
print(class_object.city)
print(class_object.emailusescurrentdata)
print(class_object.array)
print(class_object.index)
print(class_object.val)

jsonStr = json.dumps(class_object.__dict__)
print("========= PRINTING VALUES FROM CONVERTED JSON STRING===========")
print(jsonStr)

file.close()
