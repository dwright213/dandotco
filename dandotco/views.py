# from datetime import datetime
from flask import Flask, render_template, request, g, abort, jsonify, json
import pytumblr, os

from IPython import embed

from dandotco import app

from dandotco.models import bolg


@app.route('/')
def home():
	bolgs_list = bolg.get_some_bolgs(100)
	return render_template('index.html', bolgs=bolgs_list)

@app.route('/bolg/<int:bolg_id>')
def view_bolg(bolg_id=0):
	bolg_getter = bolg.get_a_bolg(bolg_id)

	# good place to put our error in a flash message, in the future
	# til then lets just give user all bolgs and hope they don't notice.
	if bolg_getter['errors']:
		print(bolg_getter['errors'])
		return render_template('index.html', bolgs=bolg_getter['bolgs'])
	single_bolg = bolg_getter['bolgs'][0]
	return render_template('single.html', bolg=single_bolg)

@app.route('/compose', methods = ['POST', 'GET'])
def compose_bolg():
	if (request.method == 'POST'):
		title = request.form['title']
		body = request.form['body']
		new_bolg = bolg.create(title, body)
		return render_template('single.html', bolg=new_bolg)
	else:
		return render_template('compose.html')

