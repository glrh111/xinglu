# -*- coding: utf-8 -*-
from app.models import User
from flask import current_app
from config import config
from app import create_app, db
from test import MyTestCase

class UserModelTestCase(MyTestCase):

	def test_password_setter(self):
		u = User(password='xiaoniao')
		self.assertTrue(u.password_hash is not None)

	def test_no_password_getter(self):
		u = User(password='suiyi')
		with self.assertRaises(AttributeError):
			u.password

	# 密码hash相关		
	def test_password_verification(self):
		u = User(password='pass1')
		self.assertTrue(u.verify_password('pass1'))
		self.assertFalse(u.verify_password('pass_other'))

	def test_password_salts_are_random(self):
		u1 = User(password='pass1')
		u2 = User(password='pass2')
		self.assertTrue(u1.password_hash != u2.password_hash)

	# 默认权限相关
	def test_default_permission(self):
		u1 = User.query.filter_by(email=current_app.config['FLASK_ADMIN']).first()
		u2 = User(email='suibianxiede@111.com')
		self.assertTrue(u1.role.name=='Administrator')
		self.assertTrue(u2.role.name!='Administrator')