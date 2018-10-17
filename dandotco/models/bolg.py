from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model
from IPython import embed

pg_db = PostgresqlDatabase(
		'dandotco',
		user='dandotco',
		password='quux',
		host='localhost',
		port=5432)

class BaseModel(Model):
	"""A base model that will use our Postgresql database"""
	class Meta:
		database = pg_db

class Bolg(BaseModel):
	title = CharField()
	body = CharField()

class Tag(BaseModel):
	name = CharField()

# crud stuff down here

def get_some_bolgs(num):
	bolgs = Bolg.select()[:num]
	dict_bolgs = []
	for bolg in bolgs:
		dict_bolgs.append(model_to_dict(bolg))

	return dict_bolgs

def get_a_bolg(bolg_id):
	query = Bolg.select()
	bolg_box = {'bolgs': [], 'errors': []}
	chosen_bolg = query.where(Bolg.id == bolg_id)
	
	if (not chosen_bolg):
		bolg_box['errors'] = 'bolg is not exists?'
		bolg_box['bolgs'] = query[:query.count()] 
		
	else:
		print('thats a valid query..')
		bolg_box['bolgs'].append(model_to_dict(chosen_bolg[0]))
		
	return bolg_box 


def create(title, body):
	try:
		bolg_one = Bolg(title=title, body=body)
		bolg_one.save()
		return bolg_one
	except:
		return 'problem(s) happened'

def get_latest():
	latest = Bolg.select().order_by(Bolg.id.desc()).first().id
	return latest