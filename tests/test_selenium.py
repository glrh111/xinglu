# -*- coding: utf-8 -*-
from selenium import webdriver
import unittest
from app import create_app, db
from app.models import User, Role, Post, Comment
import logging
import threading
from flask import url_for

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start chrome
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # if start failed, skip those test cases
        if cls.client:
            # create app
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # forbid logging
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create DB
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # add administrator
            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='exam@exam.org',\
                         username='exam_admin',\
                         password='caaaaat',\
                         role=admin_role)
            db.session.add(admin)
            db.session.commit()

            # open a thread in which Flask run
            threading.Thread(target=cls.app.run).start()

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # close server and Chrome
            cls.client.get(url_for('main.shutdown'))
            cls.client.close()

            # drop DB
            db.drop_all()
            db.session.remove()

            # delete contest
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # index page
        self.client.get(url_for('main.index'))
        self.assertTrue(self.client.status_code==200)

        # log in page
        self.client.find_element_by_link_text(u'登录').click() 
        self.assertTrue(self.client.status_code==200)

        # log in 
        self.client.find_element_by_name(u'电子邮箱/用户名').send_keys('exam@exam.org')
        self.client.find_element_by_name(u'密码').send_keys('caaaaat')
        self.client.find_element_by_name(u'登录').click()
        self.assertTrue(self.client.status_code==200)