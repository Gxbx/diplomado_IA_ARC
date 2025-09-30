from flask_restx import Api
from flask_cors import CORS

api = Api(
    version="1.0",
    title="ML API",
    description="API para servir modelos de ML (Titanic como ejemplo).",
    doc="/docs",  # Swagger UI
)
def init_extensions(app):
    CORS(app)
    api.init_app(app)
