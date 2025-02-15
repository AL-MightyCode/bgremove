from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Explicitly get port from environment or use default
    port = os.environ.get('PORT')
    if port is None:
        port = 8080
    else:
        port = int(port)
    
    app.run(host='0.0.0.0', port=port, debug=False)
