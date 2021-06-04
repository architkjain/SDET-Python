import jsonpath
import requests
import unittest
import json


class APITest(unittest.TestCase):
    def test1(self):
        url = "https://reqres.in/api/users"
        # send Get Request
        params = {"name": "AutoTestUser10001", "job": "testing"}
        response = requests.post(url, data=params)
        json_response = json.loads(response.text)

        # Verify the status code
        self.assertEqual(response.status_code, 201)
        print(response.text)
        var = jsonpath.jsonpath(json_response, 'id')
        print(var)
        var = jsonpath.jsonpath(json_response, 'createdAt')
        print(var)


if __name__ == "__main__":
    unittest.main()
