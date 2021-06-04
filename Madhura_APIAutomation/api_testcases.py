import unittest
import requests


class ApiTesting(unittest.TestCase):

    def test_count_the_id_01(self):
        url = "https://reqres.in/api/users?page=1"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Result of test case1:")
        print(response.text)

        for record in response.json()['data']:
            if record['id'] == 6:
                print("total records are correct ie 6")

        assert (response.status_code == 200), "Status code is not 200. Rather found : " + str(response.status_code)

    def test_count_the_id_03(self):
        url = "https://reqres.in/api/users/23"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Result of test case3 :", response.status_code)

    def test_print_the_details_04(self):
        url = "https://reqres.in/api/unknown"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        print("Result of test case 4:")
        for record in response.json()['data']:
            print(record['name'], record['year'])

    def test_create_user_02(self):
        url = "https://reqres.in/api/users?name=AutoTestUser&job=testing"
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload)
        print("Result of test case 2: ", response.json()['createdAt'])

    def test_print_status_05(self):
        url = "https://reqres.in/api/login"
        payload = {}
        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload)
        print("Result of test case 5: ",response.status_code)