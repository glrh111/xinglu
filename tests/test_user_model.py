# -*- coding: utf-8 -*-
import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
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

	# 确认邮件相关
	def test_confirmed_default(self):
		u = User(password='suijide')
		self.assertFalse(u.confirmed)

	def test_confirmed_right(self):
		u = User(password='suiyiqide')
		token = u.generate_confirmation_token()
		self.assertTrue(u.confirm(token))
		self.assertTrue(u.confirmed)