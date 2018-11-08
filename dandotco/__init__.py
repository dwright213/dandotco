from flask import Flask

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config.from_pyfile('settings.cfg', silent=False)

app.config.from_mapping(
	# a default secret that should be overridden by instance config
	SECRET_KEY=app.config.get('SECRET_KEY'),
	# store the database in the instance folder
	# DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)



import dandotco.views
import dandotco.auth


app.register_blueprint(auth.bp)


