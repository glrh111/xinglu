import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'a n string haha aha'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASK_MAIL_SUBJECT_PREFIX = '[glrh11]'
	FLASK_MAIL_SENDER = 'glrh11 <glrh11_test@163.com>'
	FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'glrh11_test@163.com'
	# locale
	BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'


	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.163.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = 'glrh11@163.com'
	MAIL_PASSWORD = 'woshishouquanma1' #'os.environ.get('MAIL_PASSWORD')'
	# SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	# SQLALCHEMY_DATABASE_URI = 'mysql://root:qwe123@123.56.250.233:3306/flask-test'
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:qwe123@123.56.250.233:5432/xiangjianhuan'
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 20
	FLASKY_COMMENTS_PER_PAGE = 10
	# QINIU related
	QINIU_ACCESS_KEY = 'NLbTTwY2zwZBHIh6sIdzlVruMV-eUDkXUnw-Ko87'
	QINIU_SECRET_KEY = 'LHCPI62Exu9m1W7zpwOzbqMSvm21hXGgjk4uXWo7'
	QINIU_BUCKET_NAME = 'flask-test'
	QINIU_PATH_PREFIX = 'http://o9hjg7h8u.bkt.clouddn.com/'

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
'development': DevelopmentConfig,
'testing': TestingConfig,
'production': ProductionConfig,

'default': DevelopmentConfig
}
