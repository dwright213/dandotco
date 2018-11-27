from flask import render_template
from dandotco import app


# note that we set the status codes explicitly
err = {}

@app.errorhandler(404)
def page_not_found(e):
	err['msg'] = '404'
	err['desc'] = 'What you were looking for is just not there.'
	return render_template('error.html', err=err), 404

@app.errorhandler(403)
def page_not_found(e):
	err['msg'] = '403'
	err['desc'] = 'Only authorized persons can go there.'
	return render_template('error.html', err=err), 403

@app.errorhandler(410)
def page_not_found(e):
	err['msg'] = '410'
	err['desc'] = 'This page has been removed and is gone forever now.'
	return render_template('error.html', err=err), 410

@app.errorhandler(500)
def page_not_found(e):
	err['msg'] = '500'
	err['desc'] = 'Our server is either can\'t process your request, or is just having a hard time in general.'
	return render_template('error.html', err=err), 500

