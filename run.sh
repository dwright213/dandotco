# export FLASK_DEBUG=true
# export FLASK_APP=dandotco
# export SETTINGS=./settings.cfg
# flask run

uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi:app