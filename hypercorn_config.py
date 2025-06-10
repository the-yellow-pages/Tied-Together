"""
Hypercorn Python configuration for Quart application
"""
import multiprocessing
import os

# Binding
bind = ["0.0.0.0:5000"]

# Number of workers - for ASGI applications, this is typically equal to CPU cores
workers = multiprocessing.cpu_count()

# Timeout settings
keep_alive = 2
graceful_timeout = 30

# Logging
loglevel = "info"
access_log = "-"  # Log to stdout
error_log = "-"   # Log to stderr
access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"

# SSL settings (if needed)
keyfile = None
certfile = None

# Development settings
if os.environ.get('ENVIRONMENT') == 'development':
    reload = True
    debug = True
else:
    reload = False
    debug = False
