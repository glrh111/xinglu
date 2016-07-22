# -*- coding: utf-8 -*-
import unittest
from app.models import User, Role
from flask import current_app, url_for, request
from config import config
from test import MyTestCase
from app import db
import json
import base64
import re

# Refer:
# http://dormousehole.readthedocs.io/en/latest/testing.html
# http://stackoverflow.com/questions/13959209/how-can-i-unit-test-this-flask-app
# http://flask.pocoo.org/docs/0.10/reqcontext/
class APITestCase(MyTestCase):

    _admin_auth = current_app.config['FLASK_ADMIN'] + ':qwe123'

    def _get_api_headers(self, auth):
        return {
            'Authorization': 
                'Basic ' + base64.b64encode(auth.encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def test_users_id(self):
        response = self.client.get(url_for('api.get_user', id=1),\
                                   headers=self._get_api_headers(self._admin_auth))
        self.assertTrue(response.status_code==200)

    def test_posts(self):
        # add a user
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(username='shangdan_1', \
                 email='daye_2@12306.com',\
                 password='dooooog',\
                 role=r)
        db.session.add(u)
        db.session.commit()

        # build a header
        headers = self._get_api_headers('daye_2@12306.com:dooooog')



        # write an empty post
        response = self.client.post(
            url_for('api.new_post'),\
            headers=headers,\
            data=json.dumps({'body':''}))
        self.assertTrue(response.status_code==400)

        # write a normal post
        response = self.client.post(
            url_for('api.new_post'),\
            headers=headers,\
            data=json.dumps({'body':'heiheihei'}))
        self.assertTrue(response.status_code==201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        # get the post id
        url_id_parttern = re.compile(r'/([0-9]+)')
        url_id = url_id_parttern.findall(url)[0]


        # get the post just now
        response = self.client.get(
            url,\
            headers=headers)
        self.assertTrue(response.status_code==200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url']==url)
        self.assertTrue(json_response['body']=='heiheihei')
        self.assertIsNotNone(json_response['body_html'])

        # update a post
        response = self.client.put(
            url_for('api.edit_post', id=url_id),\
            headers=headers,\
            data=json.dumps({'body':'update version'}))
        self.assertTrue(response.status_code==200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['body']=='update version')

        # get post comments
        response = self.client.get(
            url_for('api.get_post_comments', id=url_id),\
            headers=headers)
        self.assertTrue(response.status_code==200)

        