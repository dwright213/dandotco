# # import psycopg2

# from flask import current_app, g
# from flask.cli import with_appcontext

# def print_stuff():
#     print('this worked')
#     print('this worked')
#     print('this worked')
#     print('this worked')

# # def get_db():
# #     if 'db' not in g:
# #         print('its not here')
# #         print('its not here')
# #         print('its not here')
# #         try:
# #             g.db = psycopg2.connect("""
# #                                     dbname='dandotco' 
# #                                     user='dandotco' 
# #                                     host='localhost' 
# #                                     password='quux'
# #                                     """)
# #             curse = db.cursor()
# #         except:
# #             curse = {}
# #             print "I am unable to connect to the database"
# #     return curse


# # def close_db(e=None):
# #     db = g.pop('db', None)

# #     if db is not None:
# #         db.close()
