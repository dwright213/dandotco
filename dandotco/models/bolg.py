from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from IPython import embed

import re, datetime, markdown

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
	perma = CharField()
	excerpt = CharField()
	body = CharField()
	body_src = CharField()
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

	# def compare(bolg_ob):

	# def update(self, **kwargs):
	# 	# print(kwargs)
	# 	return self


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

def get_by_perma(perma):
	permad = Bolg.select().where(Bolg.perma == perma).first()
	dict_permad = model_to_dict(permad)
	dict_permad['tags'] = permad.tags()
	return dict_permad

def create(title, body, tags, **kwargs):
	tags_found = []
	if (tags):
		tags_found = tags_create(tags)

	clean_title = title.strip()
	clean_title = re.sub(r'\s{2,}', ' ', clean_title)

	if ('perma' in kwargs) and (len(kwargs['perma']) > 1):
		perma = re.sub(r"[()\"\\#/@;:<>{}`+=~|.!?,]", "", kwargs['perma'])
	else:
		perma = re.sub(r"[()\"\\#/@;:<>{}`+=~|.!?,]", "", clean_title)


	perma = (perma.replace(' ', '-')
			.replace('--', '')
			.lower())

	if (len(perma)>50):
		perma = perma[:50]

	permad = Bolg.select().where(Bolg.perma == perma)
	if (permad.count()):
		num = (permad.count() + 1)
		perma = (perma + '-' + str(num))


	if ('excerpt' in kwargs) and (len(kwargs['excerpt']) > 1):
		excerpt = kwargs['excerpt']
	else:
		excerpt = re.sub(r"[#>\n\t]", "", body.split('.', 1)[0]).strip().capitalize()
		excerpt = markdown.markdown(excerpt + '.')

	body_html = markdown.markdown(body)


	try:
		new_bolg = Bolg(title=clean_title, perma=perma, excerpt=excerpt, body=body_html, body_src=body)
		new_bolg.save()
		for tag_found in tags_found:
			tagging_create(new_bolg.id, tag_found.id)

		return get_a_bolg(new_bolg.id)
	except:
		return 'problems happened whist creating a bolg.'

def edit(bolg_id, **kwargs):

	chosen_bolg = Bolg.get(Bolg.id == bolg_id)
	dict_bolg = model_to_dict(chosen_bolg)
	proposed_edits = dict(**kwargs)

	print(chosen_bolg)
	if ('tags' in proposed_edits):
		tag_list = list(set([tag.strip() for tag in kwargs['tags'].split(',')]))
		proposed_edits.pop('tags')
		if (tag_list != chosen_bolg.tags()):
			tags_edit(bolg_id, tag_list, chosen_bolg.tags())


	for edit in proposed_edits.keys():
		if (dict_bolg[edit] == proposed_edits[edit]):
			print("no edit for the following:")
			print(edit)
			# proposed_edits.pop(edit, None)

	chosen_bolg = Bolg.update(**proposed_edits).where(Bolg.id == bolg_id)
	chosen_bolg.execute()

	return get_a_bolg(bolg_id)


# TAG STUFF

# diffs and creates/deletes a bolg's tags as necessary.
def tags_edit(bolg_id, new_list, old_list):
	old_list = [str(tag) for tag in old_list]
	
	all_list = set(new_list + old_list)
	add_list = set(new_list) - set(old_list)
	remove_list = set(old_list) - set(new_list)

	created_list = []
	for tag in add_list:
		created_list.append(tag_create(tag))

	for tag in created_list:
		tagging_create(bolg_id, tag.id)

	for tag in remove_list:
		tag_id = Tag.select().where(Tag.name == tag).first().id
		Tagging.delete().where((Tagging.bolg == bolg_id) and (Tagging.tag == tag_id)).execute()

	for tag in remove_list:
		current_tag = Tag.get(Tag.name==tag)
		used = Tagging.select().where(Tagging.tag == current_tag.id)
		if not used.count():
			print('tag %s removed' %(current_tag.name))
			current_tag.delete_instance()


# make and return a list of tags from a string provided by user
def tags_create(tag_string):
	tag_list = []
	for tag in tag_string.split(','):
		cleaned_tagname = tag.strip()
		current_tag = Tag.select().where(Tag.name == cleaned_tagname)

		# if this tag already exists, use that existent one.
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

# def tagging_remove()