from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
# from . import tag
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




class Bolg(BaseModel):
	title = CharField()
	body = CharField()

	def tags(self):
		print('okay good work we called a class level function')
		return (Tag
			.select()
			.join(Tagging, on=Tagging.tag)
			.where(Tagging.bolg == self)
			.order_by(Tag.name)
			.dicts())






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
		dict_bolgs.append(model_to_dict(bolg))

	return dict_bolgs

def get_a_bolg(bolg_id):
	query = Bolg.select()
	bolg_box = {'bolgs': [], 'errors': [], 'tags': []}
	chosen_bolg = query.where(Bolg.id == bolg_id)
	
	if (not chosen_bolg):
		bolg_box['errors'] = 'bolg is not exists?'
		bolg_box['bolgs'] = query[:query.count()] 
		
	else:
		print('thats a valid query..')
		bolg_box['bolgs'].append(model_to_dict(chosen_bolg[0]))
	print(chosen_bolg[0].tags())
	
	for blah in chosen_bolg[0].tags():
		bolg_box['tags'].append(blah)

	return bolg_box 

def get_latest():
	latest = Bolg.select().order_by(Bolg.id.desc()).first().id
	return latest


def create(title, body, tags):
	# move all this tag stuff out to its own section/file/whatever, 
	# once this works.

	tag_ids = []

	if (tags):
		for tag in tags.split(','):
			cleaned_tagname = tag.strip()
			query = Tag.select()
			existing_tag = query.where(Tag.name == cleaned_tagname)

			if (not existing_tag.first()):
				# CREATE NEW TAG, THEN RETURN IT
				fresh_tag = tag_create(tag)
				existing_tag = fresh_tag	
			
			else:
				existing_tag = existing_tag.first()
				
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