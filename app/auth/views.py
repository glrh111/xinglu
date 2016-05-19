# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask.ext.login import login_required, login_user, logout_user
from ..models import User
from .. import db
from .forms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
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
		user = User(email=form.email.data, username=form.username.data, password=form.password.data)
		db.session.add(user)
		flash(u'注册成功，请登录')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form = form)



@auth.route('/secret')
@login_required
def secret():
	return u'未登录，不能访问。:)'