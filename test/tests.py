import unittest
from dandotco.models.bolg import *


# all models should return data in string, list, or dict format, so we can 
# avoid bringing models themselves into our router. this will keep biz 
# logic in the model files and simplify our router.

MODELS = [Bolg, Tag, Tagging]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class BolgTagTest(unittest.TestCase):

	def setUp(self):
		test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
		test_db.connect()
		test_db.create_tables(MODELS)

		self.test_bolg = create( 
							title='yo', 
							body='mtv raps',
							tags='Ed Lover, Dr. Dre')
	def tearDown(self):
		test_db.drop_tables(MODELS)
		test_db.close()
		print('tests is done')


	def test_bolg_tags_number(self):
		"""
		test that bolg creation also creates correct number of tags
		"""
		tags = self.test_bolg.tags()
		self.assertEqual(len(tags), 2)


	def test_bolg_tags(self):
		"""
		test that bolg.tags gets us the correct tags
		"""
		tags = self.test_bolg.tags()
		self.assertItemsEqual(tags, [u'Ed Lover', u'Dr. Dre'])