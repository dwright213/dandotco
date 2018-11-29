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


#### update: vuejs

I think it would be funny to modern tech (Vuejs, Sass, flexbox, etc) to build a solidly responsive, accessible, and dynamic front end, but stick with the stock browser styles for background colors, fonts, link behavior, and all the rest.

With Vue, my favored approach is to use webpack's "chunking" feature to make different js files for different pages. So we still route with flask, but vue and axios are pulling the data in, via paralell api routes. 


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
