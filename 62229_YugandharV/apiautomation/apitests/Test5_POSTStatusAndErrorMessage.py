import jsonpath
import requests
import unittest
import json


class APITest(unittest.TestCase):
    def test1(self):
        url = "https://reqres.in/api/login"
        # send Get Request
        params = {"email": "peter@klaven"}

        response = requests.post(url, data=params)
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    unittest.main()
