from flask import request
from flask_restx import Namespace, Resource
from .schemas import PredictPayload
from .services import predict_one, get_metadata

ns = Namespace("titanic", description="Predicción de supervivencia (Titanic)")

# Modelos para Swagger
ns.models[PredictPayload.name] = PredictPayload

@ns.route("/check")
class Health(Resource):
    @ns.doc("check")
    def get(self):
        meta = get_metadata()
        return {
            "status": "ok",
            "model_version": meta.get("version"),
            "metrics_test": meta.get("metrics_test"),
        }, 200

@ns.route("/predict")
class Predict(Resource):
    @ns.expect(PredictPayload, validate=True)
    @ns.doc("predict")
    def post(self):
        """
        Predicción de supervivencia a partir de características de un pasajero.
        """
        payload = request.json or {}
        out = predict_one(payload)
        return out, 200
