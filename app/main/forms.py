# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField, \
    BooleanField, PasswordField, FileField
from flask.ext.pagedown.fields import PageDownField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import Role

class EditProfileForm(Form):
    name = StringField(u'姓名', validators=[Length(0, 64)])
    password = PasswordField(u'密码')
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人介绍')

    # 用户头像通过另外的实现
    # head_portrait = FileField(u'用户头像')
    submit = SubmitField(u'保存修改')

class EditProfileAdminForm(Form):
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) \
            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    email = StringField(u'电子邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField(u'用户名', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, u'用户名只能包含字母、数字、点、下划线')])
    password = PasswordField(u'密码')

    role = SelectField(u'角色', coerce=int)
    # confirmed = BooleanField(u'是否验证邮箱')

    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'位置', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个人介绍')
    submit = SubmitField(u'保存修改')

    def validate_email(self, field):
        if field.data != self.user.email and \
            User.query.filter_by(email=field.data).first():
            raise ValidationError(u'该邮箱已被使用，请更换邮箱注册或直接登录！')

    def validate_username(self, field):
        if field.data != self.user.username and \
            User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被该网站注册，请更换用户名注册或直接登录！')

class PostForm(Form):
    body = PageDownField(u'Come on，发个状态让大家乐呵乐呵！', validators=[Required()])
    submit = SubmitField(u'发表')

class CommentForm(Form):
    body = StringField('', validators=[Required()])
    submit = SubmitField(u'评论')