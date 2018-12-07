# from datetime import datetime
from flask import Flask, flash, render_template, request, g, abort, jsonify, json, session
from flask import Response
import os

from IPython import embed
from dandotco import app
from dandotco.models import bolg, error

@app.before_request
def before_request():
	if (not session):
		g.logged = False
	else:
		g.logged = True

@app.errorhandler(error.InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/')
def home():
	

	bolgs = bolg.get_some_bolgs(20)
	return render_template('index.html', bolgs=bolgs, route_name='home')

@app.route('/about')
def about():
	page = bolg.get_page('about')
	return render_template('single.html', bolg=page, route_name='bolg')

@app.route('/research')
def research():
	page = bolg.get_page('research')
	return render_template('single.html', bolg=page, route_name='bolg')

@app.route('/bolg/<perma>')
def view_bolg(perma):
	chosen_bolg = bolg.get_by_perma(perma)
	return render_template('single.html', bolg=chosen_bolg, route_name='bolg')

@app.route('/tagged/<tag_name>')
def tagged(tag_name):
	tagged_bolgs = bolg.tag_name_search(tag_name)
	# bolgs = tagged_bolgs['results']
	return render_template('index.html', route_name='home', bolgs=tagged_bolgs, tag_name=tag_name)


@app.route('/tagz/<search_term>')
def tagz_experiment(search_term):

	resp = jsonify(bolg.tag_name_search(search_term))
	print(search_term)
	print(resp)
	raise error.InvalidUsage('This view is gone', status_code=410)
	return resp