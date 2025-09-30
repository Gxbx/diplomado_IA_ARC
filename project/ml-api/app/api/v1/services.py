from flask import current_app as app
import json, joblib, threading, pandas as pd

_model = None
_model_lock = threading.Lock()
_metadata = None

def _load_artifacts():
    global _model, _metadata
    with _model_lock:
        if _model is None:
            _model = joblib.load(app.config["MODEL_PATH"]) #Aqui estaba el error, por autocompletado no se cargaba bien el modelo
        if _metadata is None:
            with open(app.config["MODEL_METADATA"], "r", encoding="utf-8") as f:
                _metadata = json.load(f)

def get_metadata():
    _load_artifacts()
    return _metadata

def predict_one(payload: dict):
    """
    Recibe un diccionario con las características de un pasajero y devuelve si sobrevivió o no.
    """
    _load_artifacts()
    # Reconstruir DataFrame con columnas que el pipeline espera (robusto a faltantes)
    meta = get_metadata()
    features = list(set(meta["features_num"] + meta["features_cat"]))
    df = pd.DataFrame([{k: payload.get(k, None) for k in features}])
    proba = _model.predict_proba(df)[:,1][0]
    pred = int(proba >= 0.5)
    return { "survived": pred, "probability": proba }