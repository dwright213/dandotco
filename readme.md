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


