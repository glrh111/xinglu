# Deployment
> Take [Centos](https://www.centos.org/) 6.4 as the basic environment.
> Take `sudo` as the prefix of bash commands if necessary.

## 1. Install This App
* Better update to Python2.7

> Refer to this [article](http://yijiebuyi.com/blog/108ae6186bb00cc708bc54f02adec277.html).

* Install [pip](https://pip.pypa.io/en/stable/) for Python2.7
* Get the flask app from Github

```bash
$ git clone http://github.com/glrh111/flask2.git
```

* Build vitual environment
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
> Refer to this [article](http://blog.csdn.net/shanzhizi/article/details/46484481).

* Install PostgreSQL

```
# add a related repo
$ rpm -Uvh http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm
$ yum update
# install
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

* Append the following lines `pg_hba.conf` of PostgreSQL

> You may find this file follow this path: `/var/lib/postgres/9.4/data/pg_hba.conf`

```
# allow all ipv4 for connecting to PostgreSQL
host all all 0.0.0.0/0 trust
```

* Uncomment and modify the following lines in `pg_hba.conf` of PostgreSQL

> You may find this file follow this path: `/var/lib/postgres/9.4/data/postgresql.conf`

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

> This app uses [SQLAlchemy](http://www.sqlalchemy.org/) as the orm for connecting with PostgresQL.

* Add the db infos to `config.py` in class `ProductionConfig`

```
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@hostname:5432/dbname'
```

* Create tables in DB

```
# activite vitual env
source venv/bin/activate

# enter flask shell
./manage.py shell

# create tables
flask> db.create_all()

# insert roles
flask> Role.insert_roles()

# exit
flask> ^D
```

## 4. Configure Nginx
1. Config config.ini
2. Start a uWSGI service

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

# nos of process
processes = 4

# threads per process
threads = 2

# open an stats port
stats = 127.0.0.1:9192
```
