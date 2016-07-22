# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request,\
                  current_app, jsonify

from . import main
from .forms import EditProfileForm, EditProfileAdminForm,\
                PostForm, CommentForm
from .. import db
from ..models import User, Role, Post, Comment, Permission 

from ..decorators import admin_required, permission_required
from flask.ext.login import login_required, current_user

import json

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('main.index'))

    # 分页功能
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(seenable=True).order_by(Post.timestamp.desc()).paginate(\
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    return render_template('index.html', form=form, posts=posts, pagination=pagination)

# user list
@main.route('/user-list', methods=['GET', 'POST'])
@login_required
def user_list():
    # 分页相关
    page = request.args.get('page', 1, type=int)
    pagination = User.query.order_by(User.id).paginate(\
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],\
        error_out=False)
    users = pagination.items

    return render_template('user_list.html', users=users, pagination=pagination, \
        endpoint='main.user_list')

# main page for each role
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

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()

        # 分页功能
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.filter_by(seenable=True).order_by(Post.timestamp.desc()).paginate(\
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items

    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts, pagination=pagination)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        if form.password:
            current_user.password = form.password.data
        current_user.location = form.location.data 
        current_user.about_me = form.about_me.data 
        db.session.add(current_user)
        flash(u'资料修改成功~~')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.password.data = ''
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=current_user._get_current_object())

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        if form.password:
            user.password = form.password.data
        # get role by id
        user.role = Role.query.get(form.role.data)
        # user.confirmed = form.confirmed.data

        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data

        db.session.add(user)
        flash(u'%s的资料修改成功' % user.name)
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.password.data = ''

    form.role.data = user.role_id
    # form.confirmed.data = user.confirmed

    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)

    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,\
                          post=post,\
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash(u'评论成功！')
        return redirect(url_for('main.post', id=post.id, page=-1))
    # 评论的分页功能
    page = request.args.get('page', 1, type=int)
    # 提交评论后显示最后一页的
    if page == -1:
        page = (post.comments.count()-1) / \
                current_app.config['FLASKY_COMMENTS_PER_PAGE']+1

    pagination = post.comments.filter_by(seenable=True).order_by(Comment.timestamp.asc()).paginate(\
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items

    return render_template('post.html', post=post, form=form,\
                           comments=comments, pagination=pagination)

@main.route('/edit-post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and\
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash(u'文章修改成功')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@main.route('/delete-post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and\
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    post.seenable = False
    db.session.add(post)
    flash(u'成功删除文章！')
    return redirect(url_for('main.user', username=post.author.username))

@main.route('/delete-comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    if current_user != comment.author and\
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    comment.seenable = False
    db.session.add(comment)
    flash(u'成功删除评论！')
    return redirect(url_for('main.post', id=comment.post_id))

# 关注相关
@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'没有这个用户')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash(u'你已经关注了这个用户')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    flash(u'已成功关注 %s。' % username)
    return redirect(url_for('main.user', username=username))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'没有这个用户')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash(u'你已经取消关注了这个用户')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    flash(u'成功取消关注 %s。' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'该用户不存在')
        return redirect(url_for('main.index'))
    # 分页
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(\
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],\
        error_out=False)
    followers = [item.follower for item in pagination.items]
    print followers
    return render_template('followers.html', user=user, title=u'关注者',\
        endpoint='main.followers', pagination=pagination,\
        followers=followers)


# 上传文件相关
from ..helpers import upload_image
@main.route('/upload-head/<username>')
@login_required
def upload_head(username):
    # get head_img_name by ajax
    head_img_name = request.args.get('head_img_name', '', type=str)

    # get user who is going to change his head_portrait
    user = User.query.filter_by(username=username).first()

    # user is None
    if user is None:
        flash(u'该用户不存在')
        return redirect(url_for('main.user_list'))
    # 非管理员或本人不得修改
    if current_user != user and not current_user.can(Permission.ADMINISTER):
        flash(u'你没有权限修改他人的头像信息')
        return redirect('main.user', username=user.username)

    # json return jsonify
    # if user is None:
    #     return jsonify(result=json.dumps(result, encoding='utf-8'))

    # upload image and get status
    img_src, status = upload_image('head', head_img_name)

    if status:
        # uploaded success
        tag = u'头像上传成功'
        # update to db
        user.head_portrait = img_src
        db.session.add(user)
    else:
        # uploaded failed
        tag = u'头像上传失败'

    flash(tag)

    return jsonify(result=json.dumps({'id':1, }, encoding='utf-8'))

# generate token
from ..helpers import generate_upload_token
@main.route('/upload-token/<prefix>')
@login_required
def upload_token(prefix):
    token = generate_upload_token(prefix)
    return jsonify(uptoken=token)

# save head url to db
@main.route('/save-head-to-db', methods=['GET', 'POST'])
@login_required
def save_head_to_db():
    head_url = request.args.get('head_url', '', type=str)
    if head_url:
        current_user.head_portrait = head_url + '-headPortraitCrop'
        db.session.add(current_user)
        return jsonify(status_code=1)
    return jsonify(status_code=0)

# save head url to db
# @main.route('/save-content-to-db', methods=['GET', 'POST'])
# @login_required
# def save_content_to_db():
#     head_url = request.args.get('content_url', '', type=str)
#     if head_url:
#         current_user.head_portrait = head_url + '-headPortraitCrop'
#         db.session.add(current_user)
#         return jsonify(status_code=1)
#     return jsonify(status_code=0)

# for selenium tests
@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'