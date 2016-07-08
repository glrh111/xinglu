# Deployment

## 1. Flask
1. Get this app
> Package Dependency

## 2. PostgreSQL
1. ha...cnf
> 0.0.0.0/0 trust
2. listen:'*'

## uWSGI
1. Config config.ini
2. Start a uWSGI service

`import flask`

## Nginx Configration
1. service nginx restart
2. chkconfig nginx on
3. emacs /etc/nginx/nginx.conf

## Deploy
1. venv
2. uwsgi config.ini