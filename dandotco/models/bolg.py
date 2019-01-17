import json
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from playhouse.postgres_ext import *

from flask import abort
from IPython import embed

from dandotco import app

import re, datetime, os, shutil

import markdown


# import logging
# logger = logging.getLogger('peewee')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.INFO)

# DATABASE CONNECTING
pg_db = PostgresqlDatabase(
		'dandotco',
		host=		 app.config.get('DB_HOST'),
		user=		 app.config.get('DB_USER'),
		password=	 app.config.get('DB_PW'),
		port=		 5432,
		autocommit=  True, 
		autorollback=True)



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
	images = JSONField(null=True)
	kind = CharField()

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

	def serialize(self, format, **kwargs):
		formatted_bolg = {}
		if (format == 'search_result'):
			
			tags_highlighted = []
			for tag in self.tags():
				if 'search_term' in kwargs:
					term = kwargs['search_term']
					html = tag.replace( term,('<strong>%s</strong>' %(term)) )
				else:
					html = tag
				tag_ob = {}
				tag_ob['name'] = tag
				tag_ob['html'] = html
				tags_highlighted.append(tag_ob)

			formatted_bolg['title'] = self.title
			formatted_bolg['perma'] = self.perma
			formatted_bolg['excerpt'] = self.excerpt
			formatted_bolg['created'] = date_formatter(self.created)
			formatted_bolg['tags'] = tags_highlighted

		elif (format == 'post'):
			formatted_bolg['title'] = self.title
			formatted_bolg['perma'] = self.perma
			formatted_bolg['body'] = self.body
			formatted_bolg['tags'] = self.tags()
			formatted_bolg['created'] = date_formatter(self.created)
			formatted_bolg['id'] = self.id

		elif (format == 'page'):
			formatted_bolg['title'] = self.title
			formatted_bolg['perma'] = self.perma
			formatted_bolg['body'] = self.body
			formatted_bolg['created'] = self.created
			formatted_bolg['id'] = self.id

		else:
			print('unrecognized format, throwing the whole thing in there.')

		return formatted_bolg

class Tagging(BaseModel):
	bolg = ForeignKeyField(Bolg, backref='bolg')
	tag = ForeignKeyField(Tag, backref='tag')
	class Meta:
		table_name = 'bolgs_tags'
		indexes = (
        	(('bolg', 'tag'), True),
        )


# BOLG STUFF

def date_formatter(date):
	pretty_date = date.strftime('%-m/%-d/%Y')

	return pretty_date


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
	bolgs = Bolg.select().where(Bolg.kind != 'page').order_by(Bolg.created.desc())[:num]
	for bolg in bolgs:
		dict_bolg = bolg.serialize('search_result') 
		dict_bolgs.append(dict_bolg)

	return dict_bolgs

def get_bolg(perma):
	lookup = Bolg.select().where((Bolg.kind == 'post') and (Bolg.perma == perma)).first()
	bolg = lookup.serialize('post')
	return bolg

def get_page(perma):
	lookup = Bolg.select().where((Bolg.kind != 'post') and (Bolg.perma == perma)).first()
	page = lookup.serialize('page')
	return page

def tag_name_search(search_term):
	tags = Tag.select().where(
		Tag.name.contains(search_term))
	
	bolg_id_set = set()
	if len(tags) > 0:
		for tag in tags:
			map(lambda x: bolg_id_set.add(x.id), tag.bolgs())

	bolg_list = []
	for bolg_id in bolg_id_set:
		bolg_list.append( Bolg.get_by_id(bolg_id).serialize('search_result', search_term=search_term))

	return bolg_list

def get_by_perma(perma):
	permad = Bolg.select().where(Bolg.perma == perma).first()
	dict_permad = model_to_dict(permad)
	dict_permad['tags'] = permad.tags()
	return dict_permad

# delete a bolg and it's images
def nope(bolg_id):
	deletion_candidate = Bolg.select().where(Bolg.id == bolg_id).first()	
	bolg_name = deletion_candidate.title

	if len(deletion_candidate.images):
		orig_dir = app.config.get('UPLOADED_PHOTOS_DEST') + 'original/' + str(bolg_id)
		proc_dir = app.config.get('UPLOADED_PHOTOS_DEST') + 'processed/' + str(bolg_id) 
		
		if os.path.isdir(orig_dir):

			try:
				shutil.rmtree(orig_dir)
				shutil.rmtree(proc_dir)

			except shutil.Error as err:
				print(err)
	
	# using our existing tags_edit function to handle tag/tagging removal.
	# we are replacing the bolg's current list of tags with '[]'
	tags_edit(bolg_id, [], deletion_candidate.tags())

	deletion_candidate.delete_instance()

	return ('"%s" is gone forever now.' % (bolg_name))

def create(title, body, kind, tags, **kwargs):
	tags_found = []
	if (tags):
		tag_list = tags.split(',')
		tags_found = tags_create(tag_list)

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
	# markdown.markdown(s, extensions=['fenced_code'])

	try:
		new_bolg = Bolg(title=clean_title, 
						perma=perma, 
						excerpt=excerpt, 
						body=body_html, 
						body_src=body,
						kind=kind,
						images=[])
		new_bolg.save()
		for tag_found in tags_found:
			tagging_create(new_bolg.id, tag_found.id)

		return get_a_bolg(new_bolg.id)
	except Exception as err:
		print(err)
		return 'problems happened whist creating a bolg.'

def edit(bolg_id, **kwargs):

	chosen_bolg = Bolg.get(Bolg.id == bolg_id)
	dict_bolg = model_to_dict(chosen_bolg)
	proposed_edits = dict(**kwargs)
	disallowed = ['body', 'id']

	if ('tags' in proposed_edits):
		tag_list = list(set([tag.strip() for tag in kwargs['tags'].split(',')]))
		proposed_edits.pop('tags')
		if (tag_list != chosen_bolg.tags()):
			tags_edit(bolg_id, tag_list, chosen_bolg.tags())

	for key in disallowed:
		proposed_edits.pop(key, None)

	if ('body_src' in proposed_edits) and (proposed_edits['body_src'] != chosen_bolg.body_src):
		proposed_edits['body'] = markdown.markdown(proposed_edits['body_src'], extensions=['attr_list'])


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

	created_list = tags_create(add_list)
	print(created_list)

	for tag in created_list:
		tagging_create(bolg_id, tag.id)

	for tag in remove_list:
		tag_id = Tag.select().where(Tag.name == tag).first().id
		taggings_list = Tagging.select().where((Tagging.bolg == bolg_id) and (Tagging.tag == tag_id))
		print('taggings this would delete:')
		for tagging in taggings_list:
			if tagging.bolg_id == bolg_id:
				Tagging.delete().where((Tagging.id == tagging.id)).execute()


# lets hold off on deleting unused tags, for the moment. 
	# for tag in remove_list:
	# 	current_tag = Tag.get(Tag.name==tag)
	# 	used = Tagging.select().where(Tagging.tag == current_tag.id)
	# 	if not used.count():
	# 		print('tag %s removed' %(current_tag.name))
	# 		current_tag.delete_instance()


# make and return a list of tags from a list of strings provided by user
def tags_create(tags):
	tag_list = []
	for tag in tags:
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

# def tagging_remove(bolg_id):
	# remove all taggings between a b