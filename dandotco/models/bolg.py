from peewee import *
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



def get_some_bolgs(num):
	query = Bolg.select()
	return query[:num]

def get_a_bolg(bolg_id):
	query = Bolg.select()
	bolg_box = {'bolgs': [], 'errors': []}
	chosen_bolg = query.where(Bolg.id == bolg_id)
	
	if (query.count() < bolg_id):
		bolg_box['errors'] = 'bolg is not exists'
		bolg_box['bolgs'] = query[:query.count()] 
		
	else:
		print('thats a valid query..')
		bolg_box['bolgs'].append(chosen_bolg[0])	

	return bolg_box 


def create(heading, meat):
	print(heading)
	print(meat)
	bolg_one = Bolg(title=heading, body=meat)
	bolg_one.save()
	return 'no work'

