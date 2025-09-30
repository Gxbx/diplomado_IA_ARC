import json, os, joblib, numpy as np, pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

def load_titanic():
    try:
        import seaborn as sns
        df = sns.load_dataset('titanic')
        src = "seaborn"
    except Exception:
        df = pd.read_csv("Titanic-Dataset.csv")
        src = "csv_local"
    return df, src

def build_dataset(df: pd.DataFrame):
    df = df.copy()
    df.columns = [c.lower() for c in df.columns]
    assert "survived" in df.columns, "No existe columna 'survived'."

    # Features candidatas (baja cardinalidad + numéricas estables)
    cols = [c for c in ['pclass','sex','age','sibsp','parch','fare','embarked','embark_town','alone'] if c in df.columns]
    X = df[cols].copy()
    y = df['survived'].astype(int)

    # Feature engineering mínimo
    if {'sibsp','parch'}.issubset(X.columns):
        X['familysize'] = X['sibsp'].fillna(0) + X['parch'].fillna(0) + 1

    num_features = [c for c in ['age','sibsp','parch','fare','familysize'] if c in X.columns]
    cat_features = [c for c in ['sex','embarked','embark_town','pclass','alone'] if c in X.columns]

    return X, y, num_features, cat_features

def build_pipeline(num_features, cat_features):
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    pre = ColumnTransformer([
        ("num", num_pipe, num_features),
        ("cat", cat_pipe, cat_features)
    ])
    clf = LogisticRegression(max_iter=200, solver="lbfgs")
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    return pipe

def main():
    out_dir = Path("project/ml-api/models")
    out_dir.mkdir(parents=True, exist_ok=True)

    df, src = load_titanic()
    X, y, num, cat = build_dataset(df)

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipe = build_pipeline(num, cat).fit(Xtr, ytr)

    pred = pipe.predict(Xte)
    proba = pipe.predict_proba(Xte)[:,1]
    metrics = {
        "accuracy": float(accuracy_score(yte, pred)),
        "f1": float(f1_score(yte, pred)),
        "auc": float(roc_auc_score(yte, proba))
    }

    # Save artifacts
    model_path = out_dir / "titanic_clf.joblib"
    meta_path = out_dir / "metadata.json"
    joblib.dump(pipe, model_path)

    metadata = {
        "model_path": str(model_path),
        "source": src,
        "features_num": num,
        "features_cat": cat,
        "target": "survived",
        "framework": "sklearn",
        "version": "1.0.0",
        "metrics_test": metrics
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"✅ Modelo guardado en: {model_path}")
    print(f"📄 Metadata: {meta_path}")
    print(f"📊 Métricas: {metrics}")

if __name__ == "__main__":
    main()