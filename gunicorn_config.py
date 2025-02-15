import os
import sys
import logging
import traceback

# Configure logging
logconfig_dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(process)d %(name)s : %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

def on_starting(server):
    """Log configuration details when Gunicorn starts."""
    logger = logging.getLogger('gunicorn.error')
    logger.info('Starting Gunicorn')
    logger.info(f'Current working directory: {os.getcwd()}')
    logger.info(f'Environment variables: PORT={os.environ.get("PORT")}')
    logger.info(f'Python path: {sys.path}')

def on_reload(server):
    """Log when Gunicorn reloads."""
    logger = logging.getLogger('gunicorn.error')
    logger.info('Reloading Gunicorn workers')

def post_fork(server, worker):
    """Log worker process details after fork."""
    logger = logging.getLogger('gunicorn.error')
    logger.info(f'Worker spawned (pid: {worker.pid})')

def worker_abort(worker):
    """Log details when a worker aborts."""
    logger = logging.getLogger('gunicorn.error')
    logger.error(f'Worker aborted (pid: {worker.pid})')
    logger.error('Traceback:\n' + ''.join(traceback.format_stack()))

# Get port from environment variable with detailed logging
logger = logging.getLogger('gunicorn.error')
port = os.environ.get('PORT')
if port is None:
    logger.error('PORT environment variable is not set!')
    port = '8000'
    logger.info(f'Using default port: {port}')
else:
    logger.info(f'Found PORT in environment: {port}')

try:
    port = int(port)
    logger.info(f'Successfully converted PORT to integer: {port}')
except ValueError as e:
    logger.error(f'Failed to convert PORT to integer: {e}')
    port = 8000
    logger.info(f'Using fallback port: {port}')

# Bind configuration
bind = f"0.0.0.0:{port}"
logger.info(f'Binding to: {bind}')

# Worker configuration
workers = 4
timeout = 120
preload_app = True
capture_output = True
enable_stdio_inheritance = True

# Logging configuration
loglevel = 'debug'  # Set to debug for maximum verbosity
accesslog = '-'
errorlog = '-'
logger.info('Gunicorn configuration loaded successfully')
