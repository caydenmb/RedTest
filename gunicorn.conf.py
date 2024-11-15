# gunicorn.conf.py

import multiprocessing

# Socket settings
bind = "0.0.0.0:8000"  # The address to which the server will bind
backlog = 2048  # The number of pending connections the server will hold

# Worker settings
workers = max(2, multiprocessing.cpu_count() * 2 + 1)  # Number of worker processes (adjust based on CPU count)
worker_class = "gthread"  # Worker type, using gthread for multi-threading capabilities
threads = 2  # Number of threads per worker
worker_connections = 1000  # Maximum number of simultaneous clients a worker can handle
max_requests = 1000  # Restart a worker after this many requests to reduce memory leakage
max_requests_jitter = 50  # Add jitter to avoid workers restarting all at once
timeout = 120  # Workers will be killed and restarted if they are idle for longer than this
graceful_timeout = 30  # Timeout for graceful worker restarts
keepalive = 2  # Keep-alive duration for HTTP connections in seconds

# Logging settings
loglevel = "debug"  # Logging level: debug, info, warning, error, critical
capture_output = True  # Capture stdout and stderr to log output
accesslog = "-"  # Access log file ("-" means output to stderr)
errorlog = "-"  # Error log file ("-" means output to stderr)
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)  # Log format for access log entries

# Environment settings
raw_env = [
    "DATABASE_URL=postgresql://user:password@localhost/dbname",  # Replace with your database URL
    "FLASK_ENV=production",  # Set the Flask environment to production
]

# Security settings
secure_scheme_headers = {
    "X-FORWARDED-PROTOCOL": "ssl",
    "X-FORWARDED-PROTO": "https",
    "X-FORWARDED-SSL": "on",
}
forwarded_allow_ips = "*"  # Allow all IPs for forwarded requests
reuse_port = False  # Reuse a port between multiple processes

# SSL settings (if using SSL)
keyfile = None  # Path to the SSL key file
certfile = None  # Path to the SSL certificate file
ssl_version = 2  # SSL version to use
cert_reqs = 0  # SSL certificate requirement level (None in this case)
ca_certs = None  # Path to CA certificate file
suppress_ragged_eofs = True  # Suppress "ragged EOF" exceptions
do_handshake_on_connect = False  # Perform SSL handshake on new connections
ciphers = None  # String specifying available ciphers

# Process naming and lifecycle
proc_name = "gunicorn_app"  # The name of the Gunicorn process
pidfile = None  # Path to the PID file
worker_tmp_dir = None  # Directory to store temporary worker files
user = 1000  # Worker process user ID
group = 1000  # Worker process group ID
umask = 0  # File creation mask
initgroups = False  # Whether to set the worker process's supplementary groups

# Lifecycle hooks
on_starting = None  # Function to run before the server starts
when_ready = None  # Function to run once the server is ready
pre_fork = None  # Function to run before a worker forks
post_fork = None  # Function to run after a worker forks
post_worker_init = None  # Function to run after a worker has initialized
worker_int = None  # Function to run when a worker receives INT or QUIT signals
worker_abort = None  # Function to run when a worker receives SIGABRT signal
pre_exec = None  # Function to run just before the worker forks the process
pre_request = None  # Function to run just before handling a request
post_request = None  # Function to run just after handling a request
child_exit = None  # Function to run when a child worker exits
worker_exit = None  # Function to run when a worker exits
nworkers_changed = None  # Function to run when the number of workers changes
on_exit = None  # Function to run when the master process exits

# Additional request parsing settings
limit_request_line = 4094  # The maximum size of HTTP request line in bytes
limit_request_fields = 100  # Maximum number of HTTP headers allowed in a request
limit_request_field_size = 8190  # Maximum size of an HTTP request header in bytes

# Request forwarding and proxy settings
proxy_protocol = False  # Enable Proxy Protocol
proxy_allow_ips = ["127.0.0.1", "::1"]  # Allowlist of IPs for proxy
forwarder_headers = ["SCRIPT_NAME", "PATH_INFO"]  # Headers to use for forwarding
