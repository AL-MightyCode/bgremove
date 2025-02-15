import os

# Get port from environment variable
port = os.environ.get('PORT', '8000')
port = int(port)

# Bind to the port
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 4
timeout = 120
preload_app = True

# Logging
loglevel = 'info'
accesslog = '-'
errorlog = '-'

# SSL configuration (if needed)
# keyfile = 'ssl/key.pem'
# certfile = 'ssl/cert.pem'
