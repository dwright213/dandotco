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

@app.route('/bolg/<perma>')
def view_bolg(perma):
	chosen_bolg = bolg.get_by_perma(perma)
	return render_template('single.html', bolg=chosen_bolg, route_name='bolg')

@app.route('/tagged/<tag_name>')
def tagged(tag_name):
	# tagged_bolgs = bolg.get_tagged(tag_name)
	return render_template('tagged.html', route_name='tagged', tag_name=tag_name)

@app.route('/by_id/<int:bolg_id>')
def bolg_by_id(bolg_id=0):
	chosen_bolg = bolg.get_a_bolg(bolg_id)
	return render_template('single.html', bolg=chosen_bolg, route_name='bolg')

