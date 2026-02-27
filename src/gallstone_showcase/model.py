"""Model helpers for gallstone risk prediction web app."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from gallstone_showcase.paths import data_csv_path

TARGET_COL = "Gallstone Status"
LEAKAGE_EXCLUDE = {
    "Aspartat Aminotransferaz (AST)",
    "Alanin Aminotransferaz (ALT)",
    "Alkaline Phosphatase (ALP)",
    "C-Reactive Protein (CRP)",
}


@dataclass(frozen=True)
class ModelBundle:
    """Container for trained model and feature metadata."""

    model: Pipeline
    feature_columns: list[str]
    feature_medians: pd.Series
    feature_min: pd.Series
    feature_max: pd.Series
    test_auc: float


def _coerce_numeric(frame: pd.DataFrame) -> pd.DataFrame:
    """Convert all columns to numeric when possible."""
    converted = frame.copy()
    for col in converted.columns:
        converted[col] = pd.to_numeric(converted[col], errors="coerce")
    return converted


def load_training_data() -> pd.DataFrame:
    """Load source CSV for model training."""
    return pd.read_csv(data_csv_path())


def select_feature_columns(frame: pd.DataFrame) -> list[str]:
    """Return non-leakage feature columns used for prediction."""
    cols: list[str] = []
    for col in frame.columns:
        if col == TARGET_COL:
            continue
        if col in LEAKAGE_EXCLUDE:
            continue
        cols.append(col)
    return cols


def train_bundle(random_state: int = 42) -> ModelBundle:
    """Train a logistic pipeline and return metadata for inference."""
    raw = load_training_data()
    frame = _coerce_numeric(raw)

    if TARGET_COL not in frame.columns:
        raise ValueError(f"Missing target column: {TARGET_COL}")

    features = select_feature_columns(frame)
    x = frame[features]
    y = frame[TARGET_COL].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        stratify=y,
        random_state=random_state,
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=5000, random_state=random_state)),
        ]
    )
    model.fit(x_train, y_train)

    prob = model.predict_proba(x_test)[:, 1]
    auc = float(roc_auc_score(y_test, prob))

    return ModelBundle(
        model=model,
        feature_columns=features,
        feature_medians=x.median(numeric_only=True),
        feature_min=x.min(numeric_only=True),
        feature_max=x.max(numeric_only=True),
        test_auc=auc,
    )


def predict_risk(bundle: ModelBundle, row: pd.DataFrame) -> float:
    """Return risk probability for a single row dataframe."""
    aligned = row.reindex(columns=bundle.feature_columns)
    score = bundle.model.predict_proba(aligned)[:, 1][0]
    return float(score)


def make_default_input(bundle: ModelBundle) -> pd.DataFrame:
    """Create a default feature row from training medians."""
    payload = {col: float(bundle.feature_medians[col]) for col in bundle.feature_columns}
    return pd.DataFrame([payload])
