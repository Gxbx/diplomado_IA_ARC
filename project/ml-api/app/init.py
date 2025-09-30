import os
from flask import Flask
from dotenv import load_dotenv
from .config import get_config
from .extensions import init_extensions, api
from .api.init import register_namespaces

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(get_config())
    init_extensions(app)
    register_namespaces(api)
    return app
