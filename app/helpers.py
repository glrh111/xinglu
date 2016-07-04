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
    return prefix + time.ctime() + '.' + ext

def upload_image(prefix, abspath):
    # modify default upload zone
    qiniu.config.set_default(default_zone=qiniu.config.zone1)

    # access two keys
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']
    # auth obj
    q = Auth(access_key, secret_key)
    # upload bucket name
    bucket_name = current_app.config['QINIU_BUCKET_NAME']

    # local file path - absolute path
    localfile = abspath

    # achieve file ext name
    try:
        match = re.finditer(r'.([0-9a-zA-Z]+)$')
        ext = match[-1].group(1)
    except:
        ext = 'jpg'

    # cloud filename
    key = generate_upload_filename(ext, prefix=prefix)
    # generate token
    token = q.upload_token(bucket_name, key, 3600)

    # upload
    ret, info = put_file(token, key, localfile)
    # generate img src
    img_src = current_app.config['QINIU_PATH_PREFIX'] + key

    return img_src, ret['key']==key