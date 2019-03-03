import json, os

from flask import Flask, render_template, request
from wand.display import display
from wand.image import Image
from IPython import embed

from dandotco import app
from dandotco.models.bolg import Bolg


"""
bolgs are going to need references to images, because so many things are gonna be way easier.
like getting all images associated with a bolg, and building their url's, based on bolg 
attributes, instead of using the os lib to go searching directories.
"""

def process(image, **kwargs):

	save_vars = image.split('/')
	get_dir = app.config.get('UPLOADED_PHOTOS_DEST') + image
	save_dir = app.config.get('UPLOADED_PHOTOS_DEST') + 'processed/' + save_vars[1] +'/'
	frontend_dir = app.config.get('PROCESSED_PHOTOS_DEST') + save_vars[1] + '/'

	image_name = save_vars[2].replace('.', '_') + '_'
	if not kwargs['overwrite']:
		add_2_bolg(save_vars[1], image_name, 'jpg', save_vars[2])

	try:
		os.mkdir(save_dir)
	except: 
		print('originals directory exists.')

	sizes = app.config.get('IMG_SIZES')

	with Image(filename=(get_dir)) as img:
		images = []
		for size in sizes:
			# what percentage of the image's width is the current size variable?
			scale = size / (img.width/100) 
			# get an int for our resize below.
			height = int((scale * .01) * img.height)
			if img.width > size:
				file_name = save_vars[2].replace('.', '_') + '_' + str(size) + '.jpg'
				if os.path.isfile(save_dir + file_name):
					print('processed version exists. Deleting.')
					os.remove(save_dir + file_name)

				with img.clone() as i:

					i.resize(size, height)
					# i.type = 'palette'
					if size < 1200:
						print('giffing up image because size is ' + str(size))
						i.format = 'gif'
						i.quantize(number_colors=24,
									colorspace_type='rgb',
									treedepth=0,
									dither=True,
									measure_error=False)
					i.format = 'jpg'
					i.compression_quality = 92
					i.save(filename=(save_dir + file_name))
					images.append(frontend_dir + file_name)

	return images

def add_2_bolg(bolg_id, img_name, img_format, orig_name):
	
	bolg = Bolg.get(Bolg.id == bolg_id)
	image_list = bolg.images
	img_id = len(bolg.images) + 1
	img = {
		'id': img_id,
		'name': img_name,
		'format': img_format,
		'orig_name': orig_name
		}
	image_list.append(img)

	updated_bolg = Bolg.update(images = image_list).where(Bolg.id == bolg_id)
	updated_bolg.execute()
	bolg = Bolg.get(Bolg.id == bolg_id)

# remove image from Bolg
def delete(bolg_id, orig_name):
	bolg = Bolg.get(Bolg.id == bolg_id)
	images = bolg.images
	axe_list = []

	for i, img in enumerate(images):

		if img['orig_name'] == orig_name:
			axe_list.append(i)

	delete_files(bolg_id, orig_name)
	images.pop(axe_list[0])
	updated_bolg = Bolg.update(images = images).where(Bolg.id == bolg_id)
	updated_bolg.execute()



# delete raw and processed version of a particular image.
def delete_files(bolg_id, filename):
	bolg = Bolg.get(Bolg.id == bolg_id)
	img_name = ''

	for img in bolg.images:
		print(img['orig_name'])
		print(filename)
		if img['orig_name'] == filename:
			img_name = img['name']

	orig_dir = (app.config.get('UPLOADED_PHOTOS_DEST') 
					+ 'original/'
					+ str(bolg_id)
					+'/') 

	proc_dir = (app.config.get('UPLOADED_PHOTOS_DEST') 
				+ 'processed/'
				+ str(bolg_id)
				+ '/')

	for size in app.config['IMG_SIZES']:
		image_to_delete = proc_dir + img_name + str(size) + '.jpg'
		if os.path.isfile(image_to_delete):
			print('deleting file ' + image_to_delete )
			os.remove(image_to_delete)
	
	if os.path.isfile(orig_dir + filename):
		print('deleting original file; ' + filename)
		os.remove(orig_dir + filename)



def namer(orig_name):
	return orig_name.replace('.', '_') + '_'

def get_images(bolg_id):

	bolg = Bolg.get(Bolg.id == bolg_id)
	bolg_imgs = {'images': bolg.images}

	return bolg_imgs