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
testbolg_perma = 'yo-mtv-raps'
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
			perma=testbolg_perma, 
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
		self.assertIn(testbolg_body, self.test_bolg['body'])



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


	def test_bolg_perma_creation(self):
		"""
		test that we are creating a dasherized, lowercased perma for our bolg model 
		even if perma field is blank.
		"""
		test_bolg = create( 
			title="Aol is my Internet pRoViDeR", 
			perma='', 
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertEqual(test_bolg['perma'], 'aol-is-my-internet-provider' )

	def test_bolg_perma_characters(self):
		"""
		test that we are creating a dasherized, lowercased perma for our bolg model ,
		with no special characters.
		"""
		test_bolg = create( 
			title='i am l33t h/\\xx0r, who l!stens to ?uestlove', 
			perma='i am l33t h/\\xx0r, who -->l!stens to ?uestlove', 
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertEqual(test_bolg['perma'], 'i-am-l33t-hxx0r-who-lstens-to-uestlove' )

	def test_bolg_perma_character_count(self):
		"""
		test that our bolg's generated permalink character count is <50.
		"""
		test_bolg = create( 
			title='Roberto Duran, Marvin Hagler, Sugar Ray Leonard, and Thomas Hearns', 
			perma='', 
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		char_length = len(test_bolg['perma'])
		self.assertEqual(char_length, 50 )

	def test_bolg_perma_unique(self):
		"""
		test that the perma is unique, so it can be used for a memorable
		bolg url.
		"""
		test_bolg_2 = create( 
			title=testbolg_title,
			perma='',
			excerpt=testbolg_excerpt, 
			body=testbolg_body,
			tags=testbolg_tags)

		self.assertNotEqual(test_bolg_2['perma'], self.test_bolg['perma'])

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
			perma=testbolg_perma,
			excerpt=' ', 
			body=testbolg_body,
			tags=testbolg_tags)
		
		self.assertIn('Important anecdotes about a cultural phenomenon.', test_bolg['excerpt'])

	def test_bolg_excerpt_not_contains_markdown(self):
		"""
		test that we are stripping some basic markdown stuff from our excerpt.
		"""
		test_bolg = create( 
			title=testbolg_title,
			perma=testbolg_perma,
			excerpt='', 
			body='''# HEADLINES,
			> block quotes
			
			''',
			tags=testbolg_tags)

		self.assertIn('Headlines, block quotes.', test_bolg['excerpt'])

	def test_bolg_perma_get_by(self):
		"""
		test that we can get bolgs by their permas, in a format useful for routing.
		"""
		test_bolg = get_by_perma('yo-mtv-raps')

		self.assertEqual(test_bolg['id'], self.test_bolg['id'])

	def test_bolg_bodysrc_saving(self):
		"""
		test that we are saving the the markdown source code of the blog's body.
		"""
		self.assertEqual(testbolg_body, self.test_bolg['body_src'])

	def test_bolg_body_source_saving(self):
		"""
		test that we are rendering html from teh markdowns.
		"""
		test_bolg = create( 
			title=testbolg_title,
			perma=testbolg_perma,
			excerpt=' ', 
			body='# Large text',
			tags=testbolg_tags)

		html = u'<h1>Large text</h1>'

		self.assertEqual(test_bolg['body'], html)


	def test_bolg_editing(self):
		"""
		test that we are able to edit/update the content of a bolg.
		"""
		new_body = "I like to rhyme, I like my beats funky I'm spunky, I like my oatmeal lumpy"
		new_perma = "thank-god-for-lysol"
		updated_bolg = edit(self.test_bolg['id'], 
							body_src=new_body, 
							perma=new_perma, 
							tags='Dr. Dre, Inspectah Deck, rza',
							title=testbolg_title)

		self.assertEqual(updated_bolg['perma'], new_perma)
		self.assertEqual(updated_bolg['body_src'], new_body)
		self.assertEqual(updated_bolg['tags'], [u'Inspectah Deck', u'Dr. Dre', u'rza'])
