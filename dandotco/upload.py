from flask import Flask, render_template, request, jsonify, session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from IPython import embed
from dandotco import app
from dandotco.models import image 
from functools import wraps

import os

from wand.image import Image
from wand.display import display

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if (not session):
			abort(403)
			# return redirect(url_for('auth.login'))
		return f(*args, **kwargs)
	return decorated_function


@app.route('/upload/<int:bolg_id>', methods=['POST'])
@login_required
def upload(bolg_id=0):

	if request.method == 'POST' and 'photo' in request.files:

		pics = dict(request.files)['photo']

		for pic in pics:
			bolg_folder = 'original/' + str(bolg_id)
			prospective_filename = (  app.config['UPLOADED_PHOTOS_DEST']  
									+ bolg_folder 
									+ '/' 
									+ pic.filename)
			
			overwrite = False
			if os.path.isfile(prospective_filename):
				print('photo exists. Deleting existing copy.')
				os.remove(prospective_filename)
				overwrite = True

			filename = photos.save(pic, folder=bolg_folder)
			processed_images = image.process(filename, overwrite=overwrite)

		bolg_imgs = {'images': image.get_images(bolg_id)}
		resp = jsonify(bolg_imgs)
		resp.headers.add('Access-Control-Allow-Origin', '*')		
		return resp

	
@app.route('/remove/<int:bolg_id>/<img_name>', methods=['POST'])
@login_required
def delete_image(img_name, bolg_id):
	if request.method == 'POST':
		image.delete(bolg_id, img_name)
		bolg_imgs = {'images': image.get_images(bolg_id)}
		resp = jsonify(bolg_imgs)
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp



