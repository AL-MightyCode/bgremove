web: gunicorn run:app --bind 0.0.0.0:$PORT --worker-class=sync --workers=4 --threads=1 --timeout=120 --log-level=debug --capture-output --enable-stdio-inheritance
