import requests
import unittest
import json


class APITest(unittest.TestCase):
    def test1(self):
        url = "https://reqres.in/api/users?page=1"
        # send Get Request
        response = requests.get(url)

        # Verify the status code
        self.assertEqual(response.status_code, 200)
        print(response.content)

        # Parse response to json format
        json_response = json.loads(response.text)

        # Verify total records in the response
        assert len(json_response['data']) == 6
        print(len(json_response['data']))


if __name__ == "__main__":
    unittest.main()
