## dandotco

#### how to run this (with flask dev server):
```
$ virtualenv venv
$ pip install -r requirements.txt
$ pip install -e .
$ export FLASK_DEBUG=true
$ export FLASK_APP=dandotco
$ fish run-flask.sh
```

#### stack

##### backend: 
python/flask, using peewee orm

##### database: 
postgres

##### frontend:
vuejs and sass, compiled by a gulp/webpack toolchain.

##### authentication:
amazon cognito

#### Things we'll need in prod:
user related stuff:
- create sudo user
- give user my publickeys
- disable root/password login

ubuntu packages:
- fish
- python-pip
- virtualenv
- node @10.x
- postgresql postgresql-contrib
- libmagickwand-dev

- psql
- nginx

### prod environment

create some dirs:

app: /home/user/dandotco
images: /var/media/img/
css: /var/media/dist/main.css
js: /var/media/dist/main.js

create psql user 'dandotco'


to run as service, you'll want a file called `/etc/systemd/system/dandotco.service` with something like this in it (depending on your setup).
```
[Unit]
Description=uWSGI instance to serve dandotco
After=network.target

[Service]
User=dwright
Group=www-data
WorkingDirectory=/var/www/dandotco
Environment="PATH=/var/www/dandotco/venv/bin"
ExecStart=/var/www/dandotco/venv/bin/uwsgi --ini uwsgi.ini

[Install]
WantedBy=multi-user.target

```