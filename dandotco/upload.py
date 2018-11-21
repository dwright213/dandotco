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
		overwrite = False
		if os.path.isfile(prospective_filename):
			print('photo exists. Deleting existing copy.')
			os.remove(prospective_filename)
			overwrite = True

		filename = photos.save(request.files['photo'], folder=bolg_folder)
		processed_images = image.process(filename, overwrite=overwrite)
		bolg_imgs = {'images': image.get_images(bolg_id)}
		resp = jsonify(bolg_imgs)
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp

	
@app.route('/remove/<int:bolg_id>/<img_name>/', methods=['POST'])
def delete_image(img_name, bolg_id):
	if request.method == 'POST':
		image.delete(bolg_id, filename)

