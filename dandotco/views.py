# from datetime import datetime
from flask import Flask, render_template, request, g, abort, jsonify, json
import pytumblr, os

from dandotco import app


@app.route('/')
def home():
	entries = os.path.join(app.static_folder, 'entries.json')
	with open(entries) as bolgs:
		data = json.load(bolgs)
	return render_template('index.html', bolgs=data)

@app.route('/tagged/<tag>')
def tagged(tag=None):
	entries = os.path.join(app.static_folder, 'entries.json')
	tag_filtered = []
	with open(entries) as bolgs:
		datas = json.load(bolgs)
		for index, data in enumerate(datas):
			for bolg_tag in data['tags']:
				if bolg_tag == tag:
					tag_filtered.append(data)
					print(bolg_tag + " == " + tag)
				

	return render_template('index.html', bolgs=tag_filtered)
