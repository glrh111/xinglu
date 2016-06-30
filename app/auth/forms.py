# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
	email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField(u'密码', validators=[Required()])
	remember_me = BooleanField(u'保持登录')
	summit = SubmitField(u'登录')

class RegisterForm(Form):
	email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64), Email()])
	username = StringField(u'用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能包含字母、数字、点、下划线')])
	# password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='密码不一致')])
	# password2 = PasswordField(u'确认密码', validators=[Required()])
	password = PasswordField(u'密码', validators=[Required()])
	submit = SubmitField(u'注册')

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已被使用，请更换')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'该用户名已被使用，请更换')
