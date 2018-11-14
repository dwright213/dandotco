from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from IPython import embed
from dandotco import app
import os

from wand.image import Image
from wand.display import display


app.config['UPLOADED_PHOTOS_DEST'] = 'dandotco/static/img'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/upload/<int:bolg_id>', methods=['POST'])
def upload(bolg_id=0):
	if request.method == 'POST' and 'photo' in request.files:
		bolg_folder = 'original/' + str(bolg_id)
		filename = photos.save(request.files['photo'], folder=bolg_folder)
		immmg = edit_image(filename)
		return render_template('upload.html', img=filename)

def edit_image(image):
	save_vars = image.split('/')
	get_path = 'dandotco/static/img/' + image
	save_path = 'dandotco/static/img/processed/%s/' %(save_vars[1])
	# print(image)
	# print(save_vars)
	# print(get_path)
	# print(save_path)
	try:
		os.mkdir(save_path)
	except: 
		print('directory exists, i guess...')

	with Image(filename=(get_path)) as img:
		print(img.size)
		for r in 1, 2, 3:
			with img.clone() as i:
				i.resize(int(i.width * r * 0.25), int(i.height * r * 0.25))
				i.rotate(90 * r)
				i.save(filename=(save_path + save_vars[2]))
	
	return 'dandotco/static/img/processed/333/orange.jpg'
	


# image dir established for dev.
# we need a way to create subdirs per bolg, so the directories end up looking like this, 
# given bolg_id is 103 and image name is orange.jpg:

# original image:
# dandotco/static/img/original/bolg-103/orange.jpg
#==> done 

# edited image(s):
# dandotco/static/img/edited/bolg-103/orange-thumbnail.jpg
# dandotco/static/img/edited/bolg-103/orange-mobile.jpg
# dandotco/static/img/edited/bolg-103/orange-blurred.jpg


# And so forth. These edited versions would be the images that are actually served out, 
# and they would of course be the result of running the original image through an 
# Image Magick filter. Probably on user request, so it doesnt bog the server down when 
# you upload a bunch of images.


# this is going to be an ajax route, vue will be the only one talking to it.
