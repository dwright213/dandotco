from dandotco.models.bolg import *
import unittest
import datetime


# all models should return data in string, list, or dict format, so we can 
# avoid bringing models themselves into our router. this will keep biz 
# logic in the model files and simplify our router.

MODELS = [Bolg, Tag, Tagging]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

testbolg_title = 'yo mtv raps'
testbolg_slug = 'yo-mtv-raps'
testbolg_body = 'Important anecdotes about a cultural phenomenon. A scientific study of the Ed Lover Dance.'
testbolg_excerpt = 'ed lover dancing intensifies'
testbolg_tags = 'Ed Lover, Dr. Dre'

class BolgTests(unittest.TestCase):

	def setUp(self):
		test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
		test_db.connect()
		test_db.create_tables(MODELS)

		self.testbolg_created = str(datetime.datetime.now().date())
		
		self.test_bolg = create( 
			title=testbolg_title, 
			slug=testbolg_slug, 
			body=testbolg_body,
			tags=testbolg_tags,
			excerpt=testbolg_excerpt, 
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
		test that even with crappy inputs, we are titling the bolgs right.
		"""
		crappy_title_bolg = create( 
			title="   im great at typing!!     :D   ", 
			excerpt=testbolg_excerpt, 
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


	def test_bolg_slug_creation(self):
		"""
		test that we are creating a dasherized, lowercased slug for our bolg model 
		even if slug field is blank.
		"""
		test_bolg = create( 
			title="Aol is my Internet pRoViDeR", 
			slug='', 
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertEqual(test_bolg['slug'], 'aol-is-my-internet-provider' )

	def test_bolg_slug_characters(self):
		"""
		test that we are creating a dasherized, lowercased slug for our bolg model ,
		with no special characters.
		"""
		test_bolg = create( 
			title='i am l33t h/\\xx0r, who l!stens to ?uestlove', 
			slug='i am l33t h/\\xx0r, who -->l!stens to ?uestlove', 
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertEqual(test_bolg['slug'], 'i-am-l33t-hxx0r-who-lstens-to-uestlove' )

	def test_bolg_slug_unique(self):
		"""
		test that the slug is unique, so it can be used for a memorable
		bolg url.
		"""
		test_bolg_2 = create( 
			title=testbolg_title,
			slug='',
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertNotEqual(test_bolg_2['slug'], self.test_bolg['slug'])

	def test_bolg_excerpt_acceptance(self):
		"""
		test that we create a bolg excerpt when given one.
		"""
		self.assertEqual(self.test_bolg['excerpt'], testbolg_excerpt)

	def test_bolg_excerpt_creation(self):
		"""
		test that we properly generate a bolg excerpt when not given one.
		"""
		test_bolg = create( 
			title=testbolg_title,
			slug=testbolg_slug,
			excerpt=' ', 
			body=testbolg_body,
			tags=testbolg_tags)
		self.assertEqual(test_bolg['excerpt'], 'Important anecdotes about a cultural phenomenon.')

	def test_bolg_slug_get_by(self):
		"""
		test that we can get bolgs by their slugs, in a format useful for routing.
		"""
		test_bolg = get_by_slug('yo-mtv-raps')

		self.assertEqual(test_bolg['id'], self.test_bolg['id'])