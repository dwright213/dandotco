from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from IPython import embed

import re, datetime

from werkzeug.security import generate_password_hash, \
     check_password_hash

# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.INFO)

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
			.order_by(Bolg.created))


class Bolg(BaseModel):
	title = CharField()
	slug = CharField()
	excerpt = CharField()
	body = CharField()
	created = DateTimeField(default=datetime.datetime.now)

	def tags(self):
		tag_list = []
		tag_objects = (Tag
						.select()
						.join(Tagging, on=Tagging.tag)
						.where(Tagging.bolg == self)
						.order_by(Tagging.id))

		map(lambda x: tag_list.append(x.name), tag_objects)
		tag_list = list(set(tag_list))
		return(tag_list)



class Tagging(BaseModel):
	bolg = ForeignKeyField(Bolg, backref='bolg')
	tag = ForeignKeyField(Tag, backref='tag')
	class Meta:
		table_name = 'bolgs_tags'
		indexes = (
        	(('bolg', 'tag'), True),
        )


# BOLG STUFF
def get_a_bolg(bolg_id):
	chosen_bolg = Bolg.select().where(Bolg.id == bolg_id).first()
	dict_bolg = []

	if (not chosen_bolg):
		print('nonexistent bolg requested')		
	else:
		dict_bolg = model_to_dict(chosen_bolg)

	dict_bolg['tags'] = chosen_bolg.tags() 
	return dict_bolg

def get_some_bolgs(num):
	dict_bolgs = []
	bolgs = Bolg.select().order_by(Bolg.id.desc())[:num]
	for bolg in bolgs:
		dict_bolg = model_to_dict(bolg)
		dict_bolg['tags'] = bolg.tags()
		dict_bolgs.append(dict_bolg)

	return dict_bolgs

def get_latest():
	latest = Bolg.select().order_by(Bolg.id.desc()).first().id
	return latest

def get_tagged(tag_name):
	current_tag = Tag.select().where(Tag.name == tag_name).first()
	tagged_bolgs = []
	for bolg in current_tag.bolgs():
		dict_bolg = model_to_dict(bolg)
		dict_bolg['tags'] = bolg.tags()
		tagged_bolgs.append(dict_bolg)
	return tagged_bolgs

def get_by_slug(slug):
	slugged = Bolg.select().where(Bolg.slug == slug).first()
	dict_slugged = model_to_dict(slugged)
	dict_slugged['tags'] = slugged.tags() 
	return model_to_dict(slugged)

def create(title, body, tags, **kwargs):
	tags_found = []
	if (tags):
		tags_found = tags_create(tags)

	clean_title = title.strip()
	clean_title = re.sub(r'\s{2,}', ' ', clean_title)

	if ('slug' in kwargs) and (len(kwargs['slug']) > 1):
		slug = re.sub(r"[()\"\\#/@;:<>{}`+=~|.!?,]", "", kwargs['slug'])
	else:
		slug = re.sub(r"[()\"\\#/@;:<>{}`+=~|.!?,]", "", clean_title)


	slug = (slug.replace(' ', '-')
			.replace('--', '')
			.lower())


	slugged = Bolg.select().where(Bolg.slug == slug)

	if (slugged.count()):
		num = (slugged.count() + 1)
		slug = (slug + '-' + str(num))


	if ('excerpt' in kwargs) and (len(kwargs['excerpt']) > 1):
		excerpt = kwargs['excerpt']
	else:
		excerpt = body.split('.', 1)[0].capitalize() + '.'


	try:
		new_bolg = Bolg(title=clean_title, slug=slug, excerpt=excerpt, body=body)
		new_bolg.save()
		for tag_found in tags_found:
			tagging_create(new_bolg.id, tag_found.id)

		return get_a_bolg(new_bolg.id)
	except:
		return 'problems happened whist creating a bolg.'



# TAG STUFF

# make and return a list of tags from a string provided by user
def tags_create(tag_string):
	tag_list = []
	for tag in tag_string.split(','):
		cleaned_tagname = tag.strip()
		current_tag = Tag.select().where(Tag.name == cleaned_tagname)

		# if this tag already exists, use the one we've got.
		if (current_tag.first()):
			current_tag = current_tag.first()
			
		else:
			current_tag = tag_create(cleaned_tagname)	

		tag_list.append(current_tag)

	return tag_list



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