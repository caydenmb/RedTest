# gunicorn.conf.py

# Server Socket
bind = '0.0.0.0:8000'  # This binds the server to all available IP addresses on port 8000
backlog = 2048         # Number of connections that can be queued

# Worker Processes
workers = 4            # Number of worker processes to handle requests
worker_class = 'sync'  # The type of worker to use, sync is the default
threads = 2            # Number of threads per worker
worker_connections = 1000  # Maximum number of simultaneous connections
max_requests = 1000    # Number of requests a worker will process before restarting
max_requests_jitter = 50  # Random jitter to avoid workers restarting at the same time
timeout = 120          # Timeout for a worker to handle a request before being killed
graceful_timeout = 30  # Time given to a worker to shut down gracefully
keepalive = 2          # The number of seconds to wait for the next request

# Logging
accesslog = '-'        # Log all access requests to stdout
errorlog = '-'         # Log errors to stdout
loglevel = 'debug'     # Set log level to debug for more verbose output
capture_output = True  # Capture stdout and stderr in log

# Security Headers
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on',
}
forwarded_allow_ips = '*'  # Allows connections from all forwarded IPs

# SSL/TLS Configuration (if applicable)
ssl_version = 2  # SSL version to use
cert_reqs = 0    # Certificate requirements (0 = optional)

# Custom Hooks (These hooks allow logging or other actions during server lifecycle)
def on_starting(server):
    print("Server is starting...")

def when_ready(server):
    print("Server is ready. Spawning workers.")

def pre_fork(server, worker):
    print(f"Pre-forking worker {worker.pid}...")

def post_fork(server, worker):
    print(f"Worker {worker.pid} has been forked.")

def worker_exit(server, worker):
    print(f"Worker with PID {worker.pid} has exited.")

def on_exit(server):
    print("Server is shutting down...")

# Assigning hooks to make sure all are callable
on_starting = on_starting
when_ready = when_ready
pre_fork = pre_fork
post_fork = post_fork
worker_exit = worker_exit
on_exit = on_exit
