import requests
from .json_encoders import payloadencoder


class Requests:
    def __init__(self, baseurl, headers=None):
        self.baseurl = baseurl
        self.headers = headers


class GET(Requests):

    def __init__(self, baseurl):
        super().__init__(baseurl)

    def sendrequest(self, endpoint, headers=None, param=None, *args):
        return requests.get(self.baseurl + endpoint, headers=headers, params=param)


class POST(Requests):

    def __init__(self, baseurl,  *args):
        super().__init__(baseurl)

    def sendrequest(self, endpoint, payload, headers, param=None, *args):
        payload = payloadencoder().encode(payload)
        return requests.post(self.baseurl + endpoint, payload, headers=headers)


class PUT(Requests):

    def __init__(self, baseurl,  *args):
        super().__init__(baseurl)

    def sendrequest(self, endpoint, resource_id, payload, headers, param=None, *args):
        payload = payloadencoder().encode(payload)
        return requests.put(self.baseurl + endpoint + '/' + resource_id, payload, headers=headers)


class DELETE(Requests):

    def __init__(self, baseurl,  *args):
        super().__init__(baseurl)

    def sendrequest(self, endpoint, resource_id, headers, param=None, *args):
        return requests.delete(self.baseurl + endpoint + '/' + resource_id, headers=headers)

