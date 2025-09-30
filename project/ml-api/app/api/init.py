from .v1.namespace import ns as ns_v1

def register_namespaces(api):
    api.add_namespace(ns_v1, path="/api/v1")

    # host: 0.0.0.0 o localhost o 127.0.0.1
    # puerto: 8000 (default Flask)
    # endpoint: /api/v1/titanic/predict
    # ejemplo: http://localhost:8000/api/v1/titanic/predict