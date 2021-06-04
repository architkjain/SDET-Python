import jsonpath
import requests
import unittest
import json


class APITest(unittest.TestCase):
    def test1(self):
        url = "https://reqres.in/api/users/23"
        # send Get Request
        response = requests.get(url)

        # Verify the status code
        print(response.status_code)
        self.assertEqual(response.status_code, 404)
        print(response.content)


if __name__ == "__main__":
    unittest.main()
