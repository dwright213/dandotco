export FLASK_DEBUG=true
export ENV=configs/production.py
export FLASK_APP=dandotco
export SETTINGS=./settings.cfg

# uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app

uwsgi --ini uwsgi.ini