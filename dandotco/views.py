# from datetime import datetime
from flask import Flask, flash, render_template, request, g, abort, jsonify, json
from flask import Response
import os

from IPython import embed
from dandotco import app
from dandotco.models import bolg


@app.route('/')
def home():
	return render_template('index.html', route_name='home')

@app.route('/bolg/<slug>')
def view_bolg(slug):
	chosen_bolg = bolg.get_by_slug(slug)
	return render_template('single.html', bolg=chosen_bolg, route_name='bolg')

@app.route('/tagged/<tag_name>')
def tagged(tag_name):
	# tagged_bolgs = bolg.get_tagged(tag_name)
	return render_template('tagged.html', route_name='tagged', tag_name=tag_name)

@app.route('/by_id/<int:bolg_id>')
def bolg_by_id(bolg_id=0):
	chosen_bolg = bolg.get_a_bolg(bolg_id)
	return render_template('single.html', bolg=chosen_bolg, route_name='bolg')


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

