from peewee import *

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
	abba = query.where(Bolg.id == bolg_id)
	
	if (query.count() < bolg_id):
		bolg_box['errors'] = 'bolg is not exists'
		bolg_box['bolgs'] = query[:query.count()] 
		
	else:
		print('thats a valid query..')
		bolg_box['bolgs'].append(abba[0])	


	return bolg_box 


# # this model contains two foreign keys to user -- it essentially allows us to
# # model a "many-to-many" relationship between users.  by querying and joining
# # on different columns we can expose who a user is "related to" and who is
# # "related to" a given user
# class Relationship(BaseModel):
#     from_user = ForeignKeyField(User, backref='relationships')
#     to_user = ForeignKeyField(User, backref='related_to')

#     class Meta:
#         # `indexes` is a tuple of 2-tuples, where the 2-tuples are
#         # a tuple of column names to index and a boolean indicating
#         # whether the index is unique or not.
#         indexes = (
#             # Specify a unique multi-column index on from/to-user.
#             (('from_user', 'to_user'), True),
#         )

# def print_stuff(times):
# 	from IPython import embed
# 	embed()
# 	for time in range(times):
# 		print(Bolg)

