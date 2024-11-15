# gunicorn.conf.py
import multiprocessing
import os

# Worker settings
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
threads = 2
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
graceful_timeout = 30
keepalive = 2

# Server socket
bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
backlog = 2048

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Debugging and logs
loglevel = "debug"
capture_output = True
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# SSL Configuration - Uncomment and adjust if SSL is enabled
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# Preloading
preload_app = False  # If True, each worker loads app before serving requests

# Environment Variables
raw_env = [
    "DATABASE_URL=postgresql://user:password@localhost/dbname",
    "FLASK_ENV=production"
]

# Hooks for deployment lifecycle management
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    server.log.info("Preparing to fork worker.")

def worker_exit(server, worker):
    server.log.info("Worker exited (pid: %s)", worker.pid)

def when_ready(server):
    server.log.info("Server is ready. Spawning workers.")

def on_exit(server):
    server.log.info("Server is exiting.")
