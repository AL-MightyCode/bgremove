from app import create_app
import logging
import sys
import os
import traceback

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for maximum verbosity
    format='%(asctime)s [%(levelname)s] %(name)s : %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger('flask_app')

try:
    # Log environment information
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"PYTHONPATH: {sys.path}")
    
    # Create the Flask application
    logger.info("Creating Flask application...")
    app = create_app()
    logger.info("Flask application created successfully")
    
    # Log Flask configuration
    logger.info(f"Flask ENV: {app.env}")
    logger.info(f"Flask DEBUG: {app.debug}")
    logger.info(f"Flask config: {app.config}")
    
except Exception as e:
    logger.error(f"Error during application startup: {e}")
    logger.error(f"Traceback: {''.join(traceback.format_tb(e.__traceback__))}")
    sys.exit(1)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 8000))
        logger.info(f"Starting Flask development server on port {port}")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        logger.error(f"Error running development server: {e}")
        logger.error(f"Traceback: {''.join(traceback.format_tb(e.__traceback__))}")
        sys.exit(1)
