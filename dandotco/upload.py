from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from IPython import embed
from dandotco import app
from dandotco.models import image 
import os

from wand.image import Image
from wand.display import display


# app.config['UPLOADED_PHOTOS_DEST'] = 'dandotco/static/img'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/upload/<int:bolg_id>', methods=['POST'])
def upload(bolg_id=0):
	if request.method == 'POST' and 'photo' in request.files:
		bolg_folder = 'original/' + str(bolg_id)
		filename = photos.save(request.files['photo'], folder=bolg_folder)
		processed_images = image.process(filename)
		return render_template('upload.html', imgs=processed_images)
	

