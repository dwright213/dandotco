import unittest
from dandotco.models.bolg import *
import datetime


# all models should return data in string, list, or dict format, so we can 
# avoid bringing models themselves into our router. this will keep biz 
# logic in the model files and simplify our router.

MODELS = [Bolg, Tag, Tagging]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

testbolg_title = 'yo'
testbolg_body = 'mtv raps'
testbolg_tags = 'Ed Lover, Dr. Dre'

class BolgTests(unittest.TestCase):

	def setUp(self):
		test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
		test_db.connect()
		test_db.create_tables(MODELS)

		self.testbolg_created = str(datetime.datetime.now().date())
		
		self.test_bolg = create( 
			title=testbolg_title, 
			body=testbolg_body,
			tags=testbolg_tags,
		)

	def tearDown(self):
		test_db.drop_tables(MODELS)
		test_db.close()
		print('tests is done')

# bolg features



	def test_bolg_title(self):
		"""
		test that we are correctly creating our test bolg's title.
		"""
		self.assertEqual(self.test_bolg['title'], testbolg_title )



	def test_bolg_title_cleaning(self):
		"""
		test that even with crappy inputs, we are titling the blogs right.
		"""
		crappy_title_bolg = create( 
			title="   im great at typing!!     :D   ", 
			body=testbolg_body,
			tags=testbolg_tags)
		self.assertEqual(crappy_title_bolg['title'], "im great at typing!! :D")



	def test_bolg_body(self):
		"""
		test that we are correctly creating our test bolg's body.
		"""
		self.assertEqual(self.test_bolg['body'], testbolg_body)



	def test_bolg_creation_date(self):
		"""
		test that bolg has creation date
		"""
		self.assertEqual(str(self.test_bolg['created'].date()), self.testbolg_created)	



	def test_bolg_tags(self):
		"""
		test that bolg.tags gets us the correct tags
		"""
		tags = self.test_bolg['tags']
		self.assertItemsEqual(tags, [u'Ed Lover', u'Dr. Dre'])



	def test_bolg_tags_number(self):
		"""
		test that bolg creation results in correct number of tags
		"""
		tags = self.test_bolg['tags']
		correct_tag_number = testbolg_tags.split(',')
		self.assertEqual(len(tags), len(correct_tag_number))


	


