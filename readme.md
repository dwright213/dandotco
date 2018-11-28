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
	python/flask because I don't need anything too fancy here. Ideally I won't need to maintain this thing much, once it's deployed.

##### database: 
	postgres for the same reasons as above. I wanted to use mongo but I have more confidence in sql at this point. 

##### backend:
	TBD but probably sass and vuejs.


#### my (very unique) schema:

bolgs
	- id
	- title
	- body

tags
	- id
	- name

bolgs_tags
	- bolg_id
	- tag_id


#### update: vuejs

I think it would be funny to modern tech (Vuejs, Sass, flexbox, etc) to build a solidly responsive, accessible, and dynamic front end, but stick with the stock browser styles for background colors, fonts, link behavior, and all the rest.

With Vue, my favored approach is to use webpack's "chunking" feature to make different js files for different pages. So we still route with flask, but vue and axios are pulling the data in, via paralell api routes. 


#### Things we'll need in prod:
user related stuff:
	- create sudo user
	- give user my publickeys
	- disable root/password login

other: 
	- install/make fish the default shell
