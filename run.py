from app import create_app
import os
import sys

# Create the Flask application
app = create_app()

# Configure logging
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    try:
        # Get port from environment variable
        port = os.environ.get('PORT')
        if port:
            port = int(port)
            app.logger.info(f"Using PORT from environment: {port}")
        else:
            port = 10000
            app.logger.info(f"No PORT in environment, using default: {port}")

        # Log the binding attempt
        app.logger.info(f"Attempting to bind to PORT: {port}")
        
        # Run the app
        app.run(host='0.0.0.0', port=port)
