# -*- coding: utf-8 -*-
import unittest
from app.models import User
from flask import current_app, url_for, request
from config import config
from test import MyTestCase

from werkzeug.test import Client
from werkzeug.testapp import test_app
from werkzeug.wrappers import BaseResponse, Request
from werkzeug.datastructures import Headers

import base64

# Refer:
# http://dormousehole.readthedocs.io/en/latest/testing.html
# http://stackoverflow.com/questions/13959209/how-can-i-unit-test-this-flask-app
# http://flask.pocoo.org/docs/0.10/reqcontext/
class APITestCase(MyTestCase):

    _auth = current_app.config['FLASK_ADMIN'] + ':qwe123'
    _client = Client(test_app, BaseResponse)
    _headers = Headers()
    _headers.add('Authorization', 'Basic ' + base64.b64encode(_auth))
    _headers.add('Accept', 'application/json')

    def test_get_users_id(self):
        req = Request(path=url_for('api.get_user', id=1), \
                      method='GET',\
                      headers=self._headers)
        print req.headers()
        response = self._client.get(req)
        print url_for('api.get_user', id=1)
        print response.status_code
        print response.headers
        # print response.data
        self.assertTrue(response.status_code==200)