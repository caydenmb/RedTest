# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
loglevel = "debug"
errorlog = "-"
accesslog = "-"
capture_output = True
