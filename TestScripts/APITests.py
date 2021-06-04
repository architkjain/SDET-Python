import requests
import json

host_url = "https://reqres.in"

#API Assignment 1
response_code = requests.get(host_url+"/api/users?page=1")
print(response_code)

response_result = (json.dumps(response_code.json(), indent=6))
print(response_result)

#API Assignment 2

Query_parameter = {	"name": "AutoTestUser",	"job": "testing"}
response_code1 = requests.post(host_url+"/api/users", data=Query_parameter)
print(response_code1)

response_result1 = (json.dumps(response_code1.json()))
print(response_result1)

#API Assignment3

response_code2 = requests.get(host_url+"/api/users/23")
print(response_code2)

#API Assignment 4

response_code3 = requests.get(host_url+"/api/unknown")
print(response_code3)
response_result3 = (json.dumps(response_code3.json()))
print(response_result3)

#API Assignment5

Query_parameter = {"email": "peter@klaven" }

response_code4 = requests.post(host_url+"/api/login", data=Query_parameter)
print(response_code4)

response_result4 = (json.dumps(response_code4.json()))
print(response_result4)


