# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import time
import re
from flask import current_app

def generate_upload_filename(ext, prefix='content'):
    '''
    prefix : head, content(default)
    filename : prefix - ctime - ext
    '''
    return prefix + '-' + time.ctime() + '.' + ext

def generate_upload_token(prefix):
    '''
    prefix: 'head' or 'content'
    return: (token, key)
    '''

    # modify default upload zone
    qiniu.config.set_default(default_zone=qiniu.config.zone1)

    # access two keys
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']
    # auth obj
    q = Auth(access_key, secret_key)
    # upload bucket name
    bucket_name = current_app.config['QINIU_BUCKET_NAME']

    # achieve file ext name
    try:
        match = re.finditer(r'.([0-9a-zA-Z]+)$', localfile)
        ext = match[-1].group(1)
    except:
        ext = 'jpg'

    # cloud filename
    # key = generate_upload_filename(ext, prefix=prefix)
    # generate token
    token = q.upload_token(bucket_name, None, 3600)

    return token

def upload_image(prefix, localfile):
    '''
    prefix: 'head' or 'content', and content by default
    abspath: abspath of localfile
    '''

    token, key = generate_upload_token(prefix, localfile)

    # upload
    ret, info = put_file(token, key, localfile)
    # generate img src
    img_src = current_app.config['QINIU_PATH_PREFIX'] + key

    return img_src, ret['key']==key

