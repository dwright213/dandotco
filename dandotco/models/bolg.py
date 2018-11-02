from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from IPython import embed

import logging
logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# DATABASE CONNECTING
pg_db = PostgresqlDatabase(
		'dandotco',
		user='dandotco',
		password='quux',
		host='localhost',
		port=5432)



# PEEWEE CLASS DEF'S
class BaseModel(Model):
	"""A base model that will use our Postgresql database"""
	class Meta:
		database = pg_db

class Tag(BaseModel):
	name = CharField()

	def bolgs(self):
		return (Bolg
			.select()
			.join(Tagging, on=Tagging.bolg)
			.where(Tagging.tag == self)
			.order_by(Bolg.title))

		


class Bolg(BaseModel):
	title = CharField()
	body = CharField()

	def tags(self):
		return (Tag
			.select()
			.join(Tagging, on=Tagging.tag)
			.where(Tagging.bolg == self)
			.order_by(Tag.name))


class Tagging(BaseModel):
	bolg = ForeignKeyField(Bolg, backref='bolg')
	tag = ForeignKeyField(Tag, backref='tag')
	class Meta:
		table_name = 'bolgs_tags'
		indexes = (
        	(('bolg', 'tag'), True),
        )


# BOLG STUFF
def get_some_bolgs(num):
	bolgs = Bolg.select()[:num]
	dict_bolgs = []
	for bolg in bolgs:

		tag_list = []
		map(lambda x: tag_list.append(x.name), bolg.tags())
		dict_bolg = model_to_dict(bolg)
		dict_bolg['tags'] = tag_list
		dict_bolgs.append(dict_bolg)

	return dict_bolgs

def get_a_bolg(bolg_id):
	query = Bolg.select()
	bolg_box = {'bolgs': [], 'errors': [], 'tags': []}
	chosen_bolg = query.where(Bolg.id == bolg_id)
	
	if (not chosen_bolg):
		bolg_box['errors'] = 'bolg is not exists?'
		bolg_box['bolgs'] = query[:query.count()] 
		
	else:
		bolg_box['bolgs'].append(model_to_dict(chosen_bolg[0]))

	
	for bolg in chosen_bolg[0].tags():
		bolg_box['tags'].append(bolg)

	return bolg_box 

def get_latest():
	latest = Bolg.select().order_by(Bolg.id.desc()).first().id
	return latest

def get_tagged(tag_name):
	current_tag = Tag.select().where(Tag.name == tag_name).first()
	tagged_bolgs = []
	for bolg in current_tag.bolgs():
		tag_list = []
		map(lambda x: tag_list.append(x.name), bolg.tags())
		dict_bolg = model_to_dict(bolg)
		dict_bolg['tags'] = tag_list
		tagged_bolgs.append(dict_bolg)


	return tagged_bolgs

def create(title, body, tags):
	# move all this tag stuff out to its own section/file/whatever, 
	# once this works.

	tag_ids = []

	if (tags):
		for tag in tags.split(','):
			cleaned_tagname = tag.strip()
			query = Tag.select()
			existing_tag = query.where(Tag.name == cleaned_tagname)

			if (existing_tag.first()):
				existing_tag = existing_tag.first()
				
			else:
				fresh_tag = tag_create(tag)
				existing_tag = fresh_tag	
			
			tag_ids.append(existing_tag.id)


	try:
		new_bolg = Bolg(title=title, body=body)
		new_bolg.save()

		for tag_id in tag_ids:
			tagging_create(new_bolg.id, tag_id)

		return new_bolg
	except:
		return 'problems happened whist creating a bolg.'



# TAG STUFF
def tag_create(name):
	try:
		new_tag = Tag(name=name)
		new_tag.save()
		return new_tag
	except:
		return 'problems happened whilst creating a tag.'



# TAGGING STUFF
def tagging_create(bolg_id, tag_id):
	try:
		new_tagging = Tagging(bolg=bolg_id, tag=tag_id)
		new_tagging.save()
	except:
		return 'problems happened whilst creating a tagging.'