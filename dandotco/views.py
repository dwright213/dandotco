# from datetime import datetime
from flask import Flask, render_template, request, g, abort, jsonify, json
import pytumblr, os

from dandotco import app

# app.static_folder = "dandotco/static"

@app.route('/')
def index():
	entries = os.path.join(app.static_folder, 'entries.json')
	with open(entries) as bolgs:
		data = json.load(bolgs)
	return render_template('index.html', bolgs=data)
