from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES

from dandotco import app

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST' and 'photo' in request.files:
		filename = photos.save(request.files['photo'])
		return filename
	return render_template('upload.html')

