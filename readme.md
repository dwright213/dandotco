## dandotco

#### how to run this:
```
$~> virtualenv venv
$~> pip install -r requirements.txt
$~> pip install -e .
$~> export FLASK_DEBUG=true
$~> export FLASK_APP=dandotco
$~> flask run
```

#### tech choices

##### backend: 
python/flask

##### database: 
postgres, with peewee orm.

##### frontend:
vuejs and sass, compiled by a gulp/webpack toolchain.

##### authentication:
amazon cognito (i'm not an infosec expert).

#### Things we'll need in prod:
user related stuff:
- create sudo user
- give user my publickeys
- disable root/password login

ubuntu packages:
- fish
- python-pip
- virtualenv
- node @10.0.0
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
