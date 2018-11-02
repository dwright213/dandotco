# from datetime import datetime
from flask import Flask, render_template, request, g, abort, jsonify, json
from flask import Response
import os

from IPython import embed

from dandotco import app

from dandotco.models import bolg

@app.route('/')
def home():
	return render_template('index.html', route_name='home')

@app.route('/bolg/<int:bolg_id>')
def view_bolg(bolg_id=0):
	bolg_getter = bolg.get_a_bolg(bolg_id)

	if bolg_getter['errors']:
		print(bolg_getter['errors'])
		return render_template('index.html', bolgs=bolg_getter['bolgs'])
	single_bolg = bolg_getter['bolgs'][0]
	tags = bolg_getter['tags']
	return render_template('single.html', bolg=single_bolg, tags=tags, route_name='bolg')

@app.route('/tagged/<tag_name>')
def tagged(tag_name):
	# tagged_bolgs = bolg.get_tagged(tag_name)
	return render_template('tagged.html', route_name='tagged', tag_name=tag_name)

@app.route('/compose', methods = ['POST', 'GET'])
def compose_bolg():
	if (request.method == 'POST'):
		title = request.form['title']
		body = request.form['body']
		tags = request.form['tags']
		new_bolg = bolg.create(title, body, tags)
		return render_template('single.html', bolg=new_bolg, route_name='bolg')
	else:
		return render_template('compose.html', route_name='compose')


# ajax routes

@app.route('/api')
def api_all():
	all_bolgs = bolg.get_some_bolgs(100)
	resp = jsonify(all_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

@app.route('/api/bolg/<int:bolg_id>')
def api_one(bolg_id=0):
	bolg_getter = bolg.get_a_bolg(bolg_id)

	if bolg_getter['errors']:
		print(bolg_getter['errors'])
		single_bolg = {'error': 'bolg not found'}
	else: single_bolg = bolg_getter['bolgs'][0]

	resp = jsonify(single_bolg)
	resp.headers.add('Access-Control-Allow-Origin', '*')

	return resp

@app.route('/api/tagged/<tag_name>')
def api_tagged(tag_name):
	tagged_bolgs = bolg.get_tagged(tag_name)
	resp = jsonify(tagged_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

