from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from IPython import embed
from dandotco import app

app.config['UPLOADED_PHOTOS_DEST'] = 'dandotco/static/img'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/upload/<int:bolg_id>', methods=['POST'])
def upload(bolg_id=0):
	if request.method == 'POST' and 'photo' in request.files:
		bolg_folder = 'original/' + str(bolg_id)
		filename = photos.save(request.files['photo'], folder=bolg_folder)
		
		return render_template('upload.html', img=filename)




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
