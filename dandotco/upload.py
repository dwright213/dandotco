from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from IPython import embed
from dandotco import app
from dandotco.models import image 
import os

from wand.image import Image
from wand.display import display



photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/upload/<int:bolg_id>', methods=['POST'])
def upload(bolg_id=0):
	if request.method == 'POST' and 'photo' in request.files:
		bolg_folder = 'original/' + str(bolg_id)
		prospective_filename = (  app.config['UPLOADED_PHOTOS_DEST']  
								+ bolg_folder 
								+ '/' 
								+ request.files['photo'].filename)
		
		print(prospective_filename)
		if os.path.isfile(prospective_filename):
			print('photo exists. Deleting existing copy.')
			os.remove(prospective_filename)

		filename = photos.save(request.files['photo'], folder=bolg_folder)
		print(filename)
		# embed()
		print(bolg_folder + '/' + request.files['photo'].filename)
		processed_images = image.process(filename)

		resp = jsonify(processed_images)
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp
		# return render_template('upload.html', imgs=processed_images)
	

