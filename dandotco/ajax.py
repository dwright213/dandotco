from functools import wraps
from IPython import embed
from dandotco.models import bolg
from warrant_lite import WarrantLite
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, jsonify
)

app = Flask(__name__)

app.config.from_pyfile('settings.cfg', silent=False)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/<int:count>', methods=['GET'], defaults)
def api_all():
	all_bolgs = bolg.get_some_bolgs(100)
	resp = jsonify(all_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

@bp.route('/api/bolg/<int:bolg_id>', methods=['GET'])
def api_one(bolg_id=0):
	bolg_getter = bolg.get_a_bolg(bolg_id)

	if bolg_getter['errors']:
		single_bolg = {'error': 'bolg not found'}
	else: single_bolg = bolg_getter['bolgs'][0]

	resp = jsonify(single_bolg)
	resp.headers.add('Access-Control-Allow-Origin', '*')

	return resp

@bp.route('/api/tagged/<tag_name>', methods=['GET'])
def api_tagged(tag_name):
	tagged_bolgs = bolg.get_tagged(tag_name)
	resp = jsonify(tagged_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

