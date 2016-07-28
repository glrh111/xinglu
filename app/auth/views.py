# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, \
	url_for, flash, current_app, jsonify
from . import auth
from flask.ext.login import login_required, login_user, logout_user, \
		current_user
from ..models import User
from .. import db
from .forms import LoginForm, RegisterForm
from ..emails import send_email
from ..decorators import admin_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			user = User.query.filter_by(username=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			# login_user(user, form.remember_me.data)
			login_user(user, remember=True, force=True)
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
	if form.validate_on_submit():
		if not form.name.data:
			form.name.data = current_app.config['DEFAULT_NAME']
		user = User(email=form.email.data, username=form.username.data, \
			password=form.password.data,\
			head_portrait=current_app.config['HEAD_PORTRAIT'], \
			name=form.name.data)
		db.session.add(user)
		flash(u'注册成功，登录以查看是否审核通过！')
		return redirect(url_for('auth.login'))
	return render_template('auth/register.html', form=form)

# 暂时不需要confirm 功能呢
@auth.route('/confirm/<int:id>/<int:suggestion>')
@login_required
@admin_required
def confirm(id, suggestion):
	user = User.query.filter_by(id=id).first()
	if user is None:
		flash(u'用户尚未注册：%s' % user.username)
	# confirmed = True: flash aready confirmed
	if user.confirmed:
		flash(u'用户已经通过审核：%s' % user.username)
	# confirmed = False: 
	else:
		# suggestion = bool(request.args.get('suggestion'))
		# request: True - confirmed = True
		if suggestion == 1:
			user.confirmed = True
			flash(u'用户通过审核：%s' % user.username)
		else:
			user.seenable = False
			flash(u'已删除用户：%s' % user.username)
		db.session.add(user)
	return redirect(url_for('auth.confirmer_list'))

@auth.route('/confirmer-list')
@login_required
@admin_required
def confirmer_list():
	confirmers = User.query.filter_by(seenable=True).filter_by(confirmed=False).all()
	return render_template('auth/confirmer_list.html', confirmers=confirmers)

@auth.before_app_request
def before_request():
	# 这里写的有问题
	# 未审核或未登录用户，只能访问首页，但是首页的外链资源加载有问题
	# 这么写的话，很麻烦，没有扩展性
	if request.endpoint:
		# api.  自有它的认证机制
		if request.endpoint[:3] != 'api':
			if current_user.is_authenticated:
				current_user.ping()
				# 审核未通过，强制退出
				if not current_user.seenable:
					logout_user()
					flash(u'你未通过审核，已经退出系统！')
					return redirect(url_for('main.index'))
				# 尚未审核，只能看首页
				if not current_user.confirmed:
					if request.endpoint not in ['main.index', 'auth.logout'] and \
						'/static/' not in request.path and \
						'clouddn' not in request.path:
						flash(u'管理员尚未审核，强迫你看首页！')
						return redirect(url_for('main.index'))
			# 未登录，只能看首页，或登录
			else:
				if request.endpoint != 'main.index' and \
						request.endpoint[:5] != 'auth.' and \
						'/static/' not in request.path and \
						'clouddn' not in request.path:
					flash(u'你未登录，强迫你看首页！')
					return redirect(url_for('main.index'))

