import jsonpath
import requests
import unittest
import json


class APITest(unittest.TestCase):
    def test1(self):
        url = "https://reqres.in/api/unknown"
        # send Get Request
        response = requests.get(url)

        # Verify the status code
        self.assertEqual(response.status_code, 200)
        print(response.content)

        # Parse response to json format
        json_response = json.loads(response.text)

        # Verify total records in the response
        assert len(json_response['data']) == 6

        records = jsonpath.jsonpath(json_response, 'data')
        datalenght = len(json_response['data'])
        for i in range(datalenght):
            name = jsonpath.jsonpath(json_response, 'data[' + str(i) + '].name')
            year = jsonpath.jsonpath(json_response, 'data[' + str(i) + '].year')
            print((name[0]), end='   ')
            print((year[0]))


if __name__ == "__main__":
    unittest.main()
