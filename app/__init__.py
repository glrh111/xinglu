# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy 
from config import config
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask.ext.bower import Bower
from flask.ext.babel import Babel, lazy_gettext

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
bower = Bower()
babel = Babel()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
# locale
# Refer To : http://www.pythondoc.com/flask-mega-tutorial/i18n.html
login_manager.login_message = lazy_gettext(\
	'Please log in to access this page.')


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	pagedown.init_app(app)
	bower.init_app(app)
	babel.init_app(app)
	app.config['BABEL_DEFAULT_LOCALE'] = 'zh'


	login_manager.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

	return app
