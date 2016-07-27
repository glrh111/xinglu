README
---------------
A brief introduction to the app

Author : `glrh11`

Email  : `glrh11@163.com`

--------------------

# Table of Content

* [Brief Introduction](#brief-introduction)
* [FrameWork](#framework)
* [RESTful API Resources](#restful-api-resources)
* [Deployment](#deployment)

# Brief Introduction

* You could register, log in or log out this site;
* You could edit your own profile;
* You could follow a registered user;
* You could publish a post with pictures powered by markdown;
* You could also comment below a specific post!

# Framework

![](http://o9hjg7h8u.bkt.clouddn.com/app%20strcture.png)

# RESTful API Resources

> Url structure: `http://hostname/api/<version>/route`
>
> Valid `<version>`: `v1.0`
>
> Access the below resources with authentication information, `http-auth` or `token` from `http://hostname/api/<version>/token`

|#|Resource URL|Method|Comment|
|---:|:---|:---:|---
|1|`/users/<int:id>`|`GET`|A user
|2|`/users/<int:id>/posts/`|`GET`|All posts by this user
|3|`/posts/`|`GET`|All posts with pagination
|4|`/posts/`|`POST`|Build a post by current authenticated user
|5|`/posts/<int:id>`|`GET`|A post
|6|`/posts/<int:id>`|`PUT`|Edit a post by current authenticated user
|7|`/posts/<int:id>/comments/`|`GET`|All comments bellow this post
|8|`/posts/<int:id>/comments/`|`POST`|Build a comment for this post by current authenticated user
|9|`/comments/`|`GET`|All comments with pagination
|10|`/comments/<int:id>`|`GET`|A comment

# Deployment

> Use [Centos](https://www.centos.org/) 6.4 as the basic environment.
>
> Use `sudo` before bash commands if necessary.

## 1. Install This App
* Better update Python to Python2.7

> Refer to this [article](http://yijiebuyi.com/blog/108ae6186bb00cc708bc54f02adec277.html).

* Install [pip](https://pip.pypa.io/en/stable/) for Python2.7

* Get this app from Github

```bash
$ git clone https://github.com/glrh111/flask2.git
```

* Build vitual environment for Flask

```bash
$ cd /path/to/your/flask/root/dir
$ chmod +x manage.py

# install vitualenv
$ pip install vitualenv

# init venv dir
$ vitualenv venv

# activite vitualenv
$ source venv/bin/activate

# install all the necessary packges
<venv>$ pip install -r requirements.txt

# install uWSGI
<venv>$ pip install uwsgi
```

> You could leave this `vitualenv` by typing `deactivate`.

## 2. Install and Configure PostgreSQL

> This app use [PostgreSQL](https://www.postgresql.org/) 9.4 as default DBMS.
>
> Refer to this [article](http://blog.csdn.net/shanzhizi/article/details/46484481).

* Install PostgreSQL

```
$ rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm
$ yum update
$ yum install postgresql94-server postgresql94-contrib
```

* Configure service (briefly)

```
# init
$ service postgresql-9.4 initdb

# start db service
$ service postgresql-9.4 start

# start once system boot
$ chkconfig postgresql-9.4 on

# add a user for this flask app
$ adduser flaskprod

# switch to default PostgreSQL user
$ su - postgres

# enter DBMS
$ psql

# set password for postgres
psql> \password postgres

# add flaskprod user and set password for her
psql> CREATE USER flaskprod WITH PASSWORD 'password';

# create DB for flaskprod
psql> CREATE DATABASE flask OWNER flaskprod;

# grant privileges for flaskprod
psql> GRANT ALL PRIVILEGES ON DATABASE flask to flaskprod;

# exit DBMS
psql> \q
```

* Append the following lines to `pg_hba.conf` of PostgreSQL

> You may find `pg_hba.conf` following this path: `/var/lib/pgsql/9.4/data/pg_hba.conf`

```
# allow all ipv4 for connecting to PostgreSQL
host all all 0.0.0.0/0 trust
```

* Uncomment and modify the following lines in `postgresql.conf` of PostgreSQL

> You may find `postgresql.conf` file following this path: `/var/lib/pgsql/9.4/data/postgresql.conf`

```
listen_addresses: '*'
```

* Restart `postgresql-9.4` service

```
$ service postgresql-9.4 restart
```

* Append following lines to `/etc/sysconfig/iptables` before the `commit` line

```
-A INPUT -m state --state NEW -m tcp -p tcp --dport 5432 -j ACCEPT
-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
```

* Restart `iptables` service

```
$ service iptables restart
```

## 3. Create DB Tables

> This app uses [SQLAlchemy](http://www.sqlalchemy.org/) as the orm for connecting to PostgreSQL.

* Add DB infos to `config.py` in class `ProductionConfig`

```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@hostname:5432/dbname'
```

* Create tables in DB

```
# activite vitual env
$ source venv/bin/activate

# enter flask shell
$ ./manage.py shell

# create tables
flask> db.create_all()

# insert roles
flask> Role.insert_roles()

# exit
flask> ^D
```

## 4. Configure Nginx

* Append the following lines to the `http` block of `/etc/nginx/nginx.conf`

```
server {
    listen 80;
    server_name your_domain_name.com;
    location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:8001;
        uwsgi_param UWSGI_CHDIR /path/to/your/flask/root/dir;
        uwsgi_param UWSGI_SCRIPT manage:app;
        root html;
        index index.html index.htm;
    }
}
```

* Restart `nginx` service

```
$ service nginx restart
```

## 5. Configure uWSGI

> Edit `config.ini` in flask root dir

```
[uwsgi]
# uWSGI connects with nginx through this socket 
socket = 127.0.0.1:8001

# app root dir
chdir = /path/to/your/flask/root/dir

# manage.py
wsgi-file = manage.py

# app name in manage.py
callable = app

# number of workers
processes = 4

# add another thread for each process
threads = 2

# open an stats port
stats = 127.0.0.1:9192
```

## 6. Start engine

* Activate vitual env

```
# activite vitual env
$ source venv/bin/activate
```

* Export some environment variabals

```
<venv>$ export FLASK_CONFIG = "production"
# DB settings, something like this:
<venv>$ export SQLALCHEMY_DATABASE_URI = "postgresql://username:password@hostname:5432/dbname"
```

* Run

```
<venv>$ uwsgi config.ini
```

> Now that the whole world could access to your zone.
>
> Exciting!