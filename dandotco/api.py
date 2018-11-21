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

@bp.route('/', methods=['GET'])
def api_latest():
	latest_bolgs = bolg.get_some_bolgs(20)
	resp = jsonify(latest_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

@bp.route('/<int:count>', methods=['GET'])
def api_all(count=20):
	some_bolgs = bolg.get_some_bolgs(count)
	resp = jsonify(some_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

@bp.route('<int:bolg_id>/images', methods=['GET'])
def api_one(bolg_id=0):
	single_bolg = bolg.get_a_bolg(bolg_id)
	resp = jsonify(single_bolg)
	print(resp)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

@bp.route('/tagged/<tag_name>', methods=['GET'])
def api_tagged(tag_name):
	tagged_bolgs = bolg.get_tagged(tag_name)
	resp = jsonify(tagged_bolgs)
	resp.headers.add('Access-Control-Allow-Origin', '*')
	return resp

