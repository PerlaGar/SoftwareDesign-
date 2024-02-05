from flask import Flask
from flask_cors import CORS

def create_app() -> Flask:
    '''Crea la aplicación principal'''
    app = Flask(__name__)
    CORS(app)
    return app