from functools import wraps
from IPython import embed
from dandotco.models import bolg
from warrant_lite import WarrantLite
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
)

app = Flask(__name__)

app.config.from_pyfile('settings.cfg', silent=False)

bp = Blueprint('auth', __name__)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if (not session):
			return redirect(url_for('auth.login'))
		return f(*args, **kwargs)
	return decorated_function


# @bp.before_request
# def before_request():
# 	if (not session):
# 		flash('NOT LOGGED IN')
# 	else:
# 		flash('LOGGED IN')


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		wl = WarrantLite(username=username, password=password,
						pool_id=app.config.get('USER_POOL_ID'),
						pool_region=app.config.get('USER_POOL_REGION'),
						client_id=app.config.get('COGNITO_CLIENT_ID'),
						client_secret=app.config.get('COGNITO_CLIENT_SECRET'))
		try:
			tokens = wl.authenticate_user()
			session.clear()
			session['user_token'] = tokens.get('AuthenticationResult')['AccessToken']
			flash('You were successfully logged in')
			return redirect(url_for('home'))
			
		except:
			flash('oops, an error happened (probably password related)')
			return render_template('login.html', route_name='login')

	else:
		session.clear()
		flash('good work logging out')


	return render_template('login.html')



@bp.route('/compose', methods = ['POST', 'GET'])
@login_required
def compose_bolg():

	if (request.method == 'POST'):
		title = request.form['title']
		perma = request.form['perma']
		excerpt = request.form['excerpt']
		body = request.form['body']
		tags = request.form['tags']
		new_bolg = bolg.create(title, body, tags, excerpt=excerpt)
		new_bolg['perma']
		return redirect(str('/bolg/'+ new_bolg['perma']))

	else:
		return render_template('compose.html', route_name='compose')


@bp.route('/edit/<id>', methods=[ 'GET', 'POST'])
@login_required
def edit_bolg(id):
	chosen_bolg = bolg.get_a_bolg(id)
	if (request.method == 'POST'):
		bolg_ob = {
			'title': request.form['title'],
			'perma': request.form['perma'],
			'excerpt': request.form['excerpt'],
			'body_src': request.form['body'],
			'tags': request.form['tags']}

		bolg.edit(chosen_bolg['id'], **bolg_ob)
		return redirect('/')

	return render_template('edit.html', bolg=chosen_bolg, route_name='edit')

