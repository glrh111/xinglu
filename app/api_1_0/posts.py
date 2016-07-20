from ..models import AnonymousUser, User, Post, Permission
from flask import g, jsonify, request, current_app
from . import api
from .authentication import auth
from .decorators import permission_required
from .errors import forbidden
from .. import db

# with pagination
@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.pagination(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    nxt = None
    if pagination.has_next:
        nxt = url_for('api.get_posts', page=page+1, _external=True)
    posts = Post.query.all()
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev, 
        'next': nxt, 
        'count': pagination.total,
        })

@api.route('/posts/<int:id>')
@auth.login_required
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

# `POST` method is used to `insert` a new `resource`
@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_posts():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
           {'Location': url_for('api.get_post', id=post.id, _external=True)}

# `PUT` method is used to `update` a `resource`
@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())