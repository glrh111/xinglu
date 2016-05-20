# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

from ..decorators import admin_required, permission_required
from ..models import Permission 
from flask.ext.login import login_required

@main.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def admin_only():
	return "for administrators only"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderator_only():
	return "for moderator only"



	