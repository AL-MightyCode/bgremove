from app import create_app
import os

# Create the Flask application
app = create_app()

# Get port with a hardcoded default
port = int(os.environ.get('PORT', 10000))
print(f"Starting with port: {port}")  # Add debug print

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
