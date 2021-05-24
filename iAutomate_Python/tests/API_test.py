# Author: Priyanka

from framework import Status
from framework import AutoTest
from framework.annotations import groupInit, groupCleanup
from components.api.api_lib import POST, GET, DELETE
from components.api.json_encoders import payloadencoder
from tests.testreusables.APIModels.Users import User
import json


@groupInit
def init():
    print('Inside groupInit()')


class TestCase_API(AutoTest):
    """ API test """
    obj_user = None
    baseurl = ''
    endpoint = ''
    headers = ''

    def set_up(self):
        self.obj_user = User('John', 'Product Manager')
        self.baseurl = self.testdata['baseurl']
        self.endpoint = self.testdata['endpoint']
        self.headers = {'Content-Type': 'application/json'}

    def test(self, *args):
        post = POST(self.baseurl)
        response = post.sendrequest(self.endpoint, self.obj_user, self.headers)

        if response.ok:
            self.log_step_result('Step 1', 'Post user data',
                                 'Verify : Status code is 201',
                                 'Status code is 201', Status.PASS)
        else:
            self.log_step_result('Step 1', 'Post user data',
                                 'Verify : Status code is 201',
                                 'Status code is NOT 201', Status.FAIL)
        print(response.text)

    def tear_down(self):
        try:
            pass
        except:
            pass


class TestCase_AHEM_API(AutoTest):
    """ API test """
    obj_user = None
    baseurl = ''
    auth_ep = ''
    emails_ep = ''
    mailbox = ''
    headers = ''

    def set_up(self):
        self.baseurl = self.testdata['baseurl']
        self.auth_ep = self.testdata['auth_ep']
        self.emails_ep = self.testdata['emails_ep']
        self.mailbox = self.testdata['mailbox']
        self.emails_ep = self.emails_ep.replace('{mailboxName}', self.mailbox)
        self.headers = {'Content-Type': 'application/json'}

    def test(self, *args):
        post = POST(self.baseurl)
        response = post.sendrequest(self.auth_ep, {}, self.headers)

        if response.ok:
            d = json.loads(response.text)
            if d['success']:
                auth_token = d['token']
                self.log_step_result('Step 1', 'Get AHEM authentication token', 'Verify : ',
                                     'authentication token received', Status.PASS)

                self.headers['Authorization'] = 'Bearer ' + auth_token
            else:
                self.log_step_result('Step 1', 'Get AHEM authentication token', 'Verify : ',
                                     'Success : False while getting authentication token', Status.FAIL)
        else:
            self.log_step_result('Step 1', 'Get AHEM authentication token', 'Verify : ',
                                 'Error while getting authentication token', Status.FAIL)

        get = GET(self.baseurl)
        response = get.sendrequest(self.emails_ep, headers=self.headers)
        if response.ok:
            d = json.loads(response.text)
            if 'error' not in d:
                self.log_step_result('Step 2', 'Email should be present', 'Verify : ',
                                     'Emails are present', Status.PASS)
            else:
                self.log_step_result('Step 2', 'Email should be present', 'Verify : ',
                                     'Emails are NOT present', Status.FAIL)
        else:
            self.log_step_result('Step 2', 'Email should be present', 'Verify : ',
                                 'Emails NOT found', Status.FAIL)

    def tear_down(self):
        pass


@groupCleanup
def clean():
    print('Inside groupCleanup()')
