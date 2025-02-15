from app import create_app
import os
import sys

# Create the Flask application
app = create_app()

# Print environment for debugging
print("Current working directory:", os.getcwd(), file=sys.stderr)
print("Available environment variables:", os.environ.keys(), file=sys.stderr)

# Get the port from environment
port = os.environ.get('PORT')
if port:
    port = int(port)
    print(f"Using PORT from environment: {port}", file=sys.stderr)
else:
    port = 8080
    print(f"No PORT in environment, using default: {port}", file=sys.stderr)

# Store port in app config
app.config['PORT'] = port

if __name__ == '__main__':
    print(f"Starting development server on port {port}", file=sys.stderr)
    app.run(host='0.0.0.0', port=port)
