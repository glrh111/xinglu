# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class NameForm(Form):
	name = StringField(u'你叫啥？', validators=[Required()])
	submit = SubmitField(u'提交')