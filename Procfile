web: gunicorn -b 0.0.0.0:$PORT -k gevent -w 3 warehouse.wsgi
worker: warehouse worker --redis rq high default low
