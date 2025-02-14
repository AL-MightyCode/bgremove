from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    CORS(app)
    
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    return app 