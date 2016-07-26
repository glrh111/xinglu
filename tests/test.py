# -*- coding: utf-8 -*-
import unittest
from app.models import User
from flask import current_app
from config import config
from app import create_app, db
from app.models import Role

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        # add administrator
        u1 = User(username='glrh11', \
                  email=current_app.config['FLASK_ADMIN'], \
                  password='qwe123',
                  confirmed=True)
        db.session.add(u1)
        db.session.commit()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()