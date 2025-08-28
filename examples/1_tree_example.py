import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

# Crear dataset ficticio de patrullajes
np.random.seed(42)
data = {
    "zona": np.random.choice(["Caribe", "Pacífico", "Amazonas"], size=50),
    "hora": np.random.choice(["Día", "Noche"], size=50),
    "clima": np.random.choice(["Bueno", "Regular", "Malo"], size=50),
    "actividad_sospechosa": np.random.choice([0, 1], size=50, p=[0.6, 0.4])  # 0 = No, 1 = Sí
}

df = pd.DataFrame(data)

# Codificación de variables categóricas
df_encoded = pd.get_dummies(df, columns=["zona", "hora", "clima"], drop_first=True)

# Dividir en train/test
X = df_encoded.drop("actividad_sospechosa", axis=1)
y = df_encoded["actividad_sospechosa"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar árbol de decisión
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Mostrar exactitud
accuracy = clf.score(X_test, y_test)

# Graficar árbol de decisión
plt.figure(figsize=(12,6))
plot_tree(clf, feature_names=X.columns, class_names=["No Sospechosa", "Sospechosa"], filled=True)
plt.show()

accuracy