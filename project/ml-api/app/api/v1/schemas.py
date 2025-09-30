from flask_restx import fields, Model

# Esquema de entrada para predicción (Titanic)

PredictPayload = Model("PredictPayload",{
    "pclass": fields.Integer(required=True, description="Clase del pasajero (1, 2, 3)"),
    "sex": fields.String(required=True, description="Sexo del pasajero (male, female)"),
    "age": fields.Float(required=False, description="Edad del pasajero (años)"),
    "sibsp": fields.Integer(required=False, description="Número de hermanos/cónyuges a bordo"),
    "parch": fields.Integer(required=False, description="Número de padres/hijos a bordo"),
    "fare": fields.Float(required=False, description="Tarifa del pasaje"),
    "embarked": fields.String(required=False, description="Puerto de embarque (C = Cherbourg, Q = Queenstown, S = Southampton)"),
    "embark_town": fields.String(required=False, description="Ciudad de embarque (Cherbourg, Queenstown, Southampton)"),
    "alone": fields.String(required=False, description="Si el pasajero viaja solo (True, False)"),
})