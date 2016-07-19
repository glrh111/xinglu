# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash, current_app
from . import auth
from flask.ext.login import login_required, login_user, logout_user, current_user
from ..models import User
from .. import db
from .forms import LoginForm, RegisterForm
from ..emails import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			user = User.query.filter_by(username=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			# login_user(user, form.remember_me.data)
			# 是否保持登录
			login_user(user, True) 
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'用户名或密码错误')
	return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout():
	logout_user()
	flash(u'已经成功退出系统！')
	return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	tip = ''
	if form.validate_on_submit():
		user = User(email=form.email.data, username=form.username.data, \
			password=form.password.data,\
			head_portrait=current_app.config['HEAD_PORTRAIT'], \
			name=form.name.data)
		db.session.add(user)
		flash(u'注册成功，登录以使用全部功能！')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

# 暂时不需要confirm 功能呢
# @auth.route('/confirm/<token>')
# @login_required
# def confirm(token):
# 	if current_user.confirmed:
# 		return redirect(url_for('main.index'))
# 	if current_user.confirm(token):
# 		flash(u'已经验证成功，谢谢！')
# 	else:
# 		flash(u'你这个验证邮件不可用，请重新验证')
# 	return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		current_user.ping()
		# 	and not current_user.confirmed \
		# 	and request.endpoint[:5] != 'auth.' \
		# 	and request.endpoint != 'static':
		# return redirect(url_for('auth.unconfirmed'))

# @auth.route('/unconfirmed')
# def unconfirmed():
# 	if current_user.is_anonymous or current_user.confirmed:
# 		return redirect(url_for('main.index'))
# 	return render_template('auth/unconfirmed.html')

# @auth.route('/confirm')
# @login_required
# def resend_confirmation():
# 	token = current_user.generate_confirmation_token()
# 	send_email(current_user.email, u'[确认邮箱]', 'auth/email/confirm', \
# 		user=current_user, token=token)
# 	flash(u'邮件已发至你邮箱，请看看' + token)
# 	return redirect(url_for('main.index'))
