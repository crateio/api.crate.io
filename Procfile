web: newrelic-admin run-program gunicorn -b 0.0.0.0:$PORT -k gevent -w 3 warehouse.wsgi
worker: newrelic-admin run-program warehouse worker --url $OPENREDIS_URL --db 1 high low
