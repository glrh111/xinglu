# -*- coding: utf-8 -*-
from ..models import AnonymousUser, User, Post, Permission
from flask import g, jsonify, request, current_app
from . import api
from .authentication import auth
from .decorators import permission_required
from .errors import forbidden
from .. import db

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    posts = user.posts
    return jsonify({
        'posts': [post.to_json for post in posts],
        'count': posts.count(),
        })

# 显示他所关注的人的一段时间的更新内容
# 暂时留着不写，哈哈哈
@api.route('/users/<int:id>/timeline/')
def get_user_timeline(id):
    pass
