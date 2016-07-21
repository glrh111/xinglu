# -*- coding: utf-8 -*-
from ..models import AnonymousUser, User, Post, Comment, Permission
from flask import g, jsonify, request, current_app
from . import api
from .authentication import auth
from .decorators import permission_required
from .errors import forbidden
from .. import db

@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page-1, _external=True)
    nxt = None
    if pagination.has_next:
        nxt = url_for('api.get_comments', page=page+1, _external=True)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev': prev, 
        'next': nxt, 
        'count': pagination.total,
        }) 

@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())


