web: gunicorn Home.wsgi:application --timeout 86400 --log-file -
release: bash release.sh
beat: celery -A Home.celery:app beat -S redbeat.RedBeatScheduler  --loglevel=DEBUG --pidfile /tmp/celerybeat.pid
worker: celery -A Home.celery:app  worker -Q default -n Home.%%h --without-gossip --without-mingle --without-heartbeat --loglevel=INFO --max-memory-per-child=512000 --concurrency=1
