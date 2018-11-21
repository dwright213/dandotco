from flask import Flask
from IPython import embed

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config.from_envvar('ENV')
app.config.from_pyfile('settings.cfg', silent=False)

app.config['IMG_SIZES'] = [400, 800, 1200]
# app.config['IMG_SIZES'] = [400]

app.config.from_mapping(
	SECRET_KEY=app.config.get('SECRET_KEY'),
)


import dandotco.api
import dandotco.auth
import dandotco.upload
import dandotco.views

app.register_blueprint(api.bp)
app.register_blueprint(auth.bp)
