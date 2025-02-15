from app import create_app
import os
import sys

# Create the Flask application
app = create_app()

# Print debug information
print("Environment variables:", dict(os.environ), file=sys.stderr)
print("Current directory:", os.getcwd(), file=sys.stderr)

# Use Render's default port 3000
port = int(os.environ.get('PORT', 3000))
print(f"Configured port: {port}", file=sys.stderr)

# Make the port available to the application
app.config['PORT'] = port

if __name__ == '__main__':
    print(f"Starting Flask app on port {port}", file=sys.stderr)
    app.run(host='0.0.0.0', port=port, debug=False)
