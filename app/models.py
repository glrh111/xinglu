# -*- coding: utf-8 -*-
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
import bleach
from markdown import markdown

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64), unique = True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	@staticmethod
	def insert_roles():
		roles = {
		'User': (Permission.FOLLOW |
			Permission.COMMENT |
			Permission.WRITE_ARTICLES, True),
		'Moderator': (Permission.FOLLOW |
			Permission.COMMENT |
			Permission.WRITE_ARTICLES |
			Permission.MODERATE_COMMENTS, False),
		'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()

	def __repr__(self):
		return '<Role %r>' % self.name


class Follow(db.Model):
	__tablename__ = 'follows'
	follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), \
		primary_key=True)
	followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), \
		primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	MODERATE_COMMENTS = 0x08
	ADMINISTER = 0x80

class User(db.Model, UserMixin):

	# 根据邮箱，提供默认权限
	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.email==current_app.config['FLASK_ADMIN']:
			self.role = Role.query.filter_by(permissions=0xff).first()
		if self.role is None:
			self.role = Role.query.filter_by(default=True).first()


	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique = True, index = True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)

	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	# default could accept func as arg, every time 
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
	# 用户头像的七牛cdn 链接
	head_portrait = db.Column(db.String(128), default='http://o9hjg7h8u.bkt.clouddn.com/favicon.ico')

	posts = db.relationship('Post', backref='author', lazy='dynamic')

	followed = db.relationship('Follow', \
								foreign_keys=[Follow.follower_id],\
								backref=db.backref('follower', lazy='joined'),
								lazy='dynamic',\
								cascade='all, delete-orphan')

	followers = db.relationship('Follow',\
								foreign_keys=[Follow.followed_id],\
								backref=db.backref('followed', lazy='joined'),\
								lazy='dynamic',\
								cascade='all, delete-orphan')

	# follow related
	def follow(self, user):
		if not self.is_following(user):
			f = Follow(follower=self, followed=user)
			db.session.add(f)

	def unfollow(self, user):
		f = self.followed.filter_by(followed_id=user.id).first()
		if f:
			db.session.delete(f)

	def is_following(self, user):
		return self.followed.filter_by(followed_id=user.id).first() is not None

	def is_followed_by(self, user):
		return self.followers.filter_by(follower_id=user.id).first() is not None

	# 生成密码的hash，并提供
	@property
	def password(self):
	    raise AttributeError('password is not a readble attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# 生成令牌并验证
	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True

	# 检查用户的权限
	def can(self, permissions):
		return self.role is not None and (self.role.permissions & permissions) == permissions

	def is_administrator(self):
		return self.can(Permission.ADMINISTER)

	# 刷新最后登录时间 last_seen
	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	# 生成虚拟用户
	@staticmethod
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py
		# generate
		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),\
					 username=forgery_py.internet.user_name(True),\
					 password=forgery_py.lorem_ipsum.word(),\
					 confirmed=True,\
					 name=forgery_py.name.full_name(),\
					 location=forgery_py.address.city(),\
					 about_me=forgery_py.lorem_ipsum.sentence(),\
					 member_since=forgery_py.date.date(True),
					 head_portrait='http://o9hjg7h8u.bkt.clouddn.com/favicon.ico')
			db.session.add(u)
			# is in afraid that username and email may be the same
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()



	# print提供便利
	def __repr__(self):
		return '<User %r>' % self.username

class Post(db.Model):
	'''
	posts
	'''
	__tablename__ = 'posts'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	# 用于将前端提交的mk渲染缓存
	body_html = db.Column(db.Text)

	# 生成虚拟文章post
	@staticmethod
	def generate_fake(count=1000):
		from random import seed, randint
		import forgery_py
		# generate
		seed()
		user_count = User.query.count()
		for i in range(count):
			u = User.query.offset(randint(0, user_count-1)).first()
			p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),\
					 timestamp=forgery_py.date.date(True),\
					 author=u)
			db.session.add(p)
			db.session.commit()

	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', \
						'code', 'em', 'i', 'li', 'ol', 'pre', 'strong',\
						'ul', 'h1', 'h2', 'h3', 'p']
		target.body_html = bleach.linkify(bleach.clean(
						markdown(value, output_format='html'),\
						tags=allowed_tags, strip=True))

# body 字段发生变化是，更新  body_html
db.event.listen(Post.body, 'set', Post.on_changed_body)



class AnonymousUser(AnonymousUserMixin):
	'''
	formal
	'''
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False

login_manager.anonymous_user = AnonymousUser