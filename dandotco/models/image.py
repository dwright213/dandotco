from IPython import embed

from dandotco import app

from wand.image import Image
from wand.display import display
import os

"""
to start with, we will make 3 versions of each uploaded image:

full width on mobile:
	480px - 30px of padding = 450px

approx 1/2 desktop width:
	~600px probably a good start.

full size but quality decreased a bit.
	maybe up to a maximum of 3840px width?
"""

"""
Functions needed for this are gonna include:
	process_image: to process the images as I upload them, for bolgs.

	process_all: for future cases where I have
	a new visual theme that requires new versions of existing images, or 
	say, I move to a new server and have to process all my images again.

"""

def process(image):
	
	save_vars = image.split('/')
	get_dir = app.config.get('UPLOADED_PHOTOS_DEST') + image
	save_dir = app.config.get('UPLOADED_PHOTOS_DEST') + 'processed/' + save_vars[1] +'/'
	frontend_dir = app.config.get('PROCESSED_PHOTOS_DEST') + save_vars[1] + '/'

	try:
		os.mkdir(save_dir)
	except: 
		print('directory exists, i guess...')

	sizes = [400, 800, 1200]

	with Image(filename=(get_dir)) as img:
		print(img.size)
		images = []
		for size in sizes:
			# what percentage of the image's width is the current size variable?
			scale = size / (img.width/100) 
			# get an int for our resize below.
			height = int((scale * .01) * img.height)
			if img.width > size:
				file_name = save_vars[2].replace('.', '_') + '_' + str(size) + '.jpg'
				with img.clone() as i:
					i.resize(size, height)
					i.save(filename=(save_dir + '/' + file_name))
					print(file_name)
					images.append(frontend_dir + file_name)

	return images

