"""English Streamlit app for gallstone risk prediction."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from gallstone_showcase.model import ModelBundle, make_default_input, predict_risk, train_bundle

st.set_page_config(page_title="Gallstone Risk App", page_icon="🩺", layout="wide")

KEY_FIELDS = [
    "Age",
    "Gender",
    "Body Mass Index (BMI)",
    "Glucose",
    "Total Cholesterol (TC)",
    "Low Density Lipoprotein (LDL)",
    "High Density Lipoprotein (HDL)",
    "Triglyceride",
    "Creatinine",
    "Vitamin D",
    "Visceral Fat Area (VFA)",
]


@st.cache_resource(show_spinner=True)
def get_bundle() -> ModelBundle:
    """Load and train model once per app session."""
    return train_bundle()


def _build_input_form(bundle: ModelBundle) -> pd.DataFrame:
    base = make_default_input(bundle)
    st.subheader("Patient Inputs")

    c1, c2 = st.columns(2)
    for i, field in enumerate(KEY_FIELDS):
        if field not in bundle.feature_columns:
            continue

        col = c1 if i % 2 == 0 else c2
        default = float(base.loc[0, field])
        min_value = float(bundle.feature_min[field])
        max_value = float(bundle.feature_max[field])

        with col:
            if field == "Gender":
                base.loc[0, field] = st.selectbox(
                    "Gender",
                    options=[0, 1],
                    index=int(round(default)),
                    format_func=lambda x: "Female (0)" if x == 0 else "Male (1)",
                )
            else:
                base.loc[0, field] = st.number_input(
                    field,
                    min_value=min_value,
                    max_value=max_value,
                    value=default,
                )

    return base


def _risk_label(score: float) -> tuple[str, str]:
    if score < 0.30:
        return "Low", "green"
    if score < 0.60:
        return "Moderate", "orange"
    return "High", "red"


def main() -> None:
    st.title("Gallstone Risk Prediction Web App")
    st.caption(
        "Routine-checkup based risk estimation (research/demo use only, not medical diagnosis)."
    )

    bundle = get_bundle()
    st.info(f"Model loaded. Holdout ROC-AUC: {bundle.test_auc:.3f}")

    row = _build_input_form(bundle)

    if st.button("Predict Risk", type="primary"):
        score = predict_risk(bundle, row)
        label, color = _risk_label(score)

        st.markdown(
            f"### Predicted Gallstone Risk: :{color}[{score * 100:.1f}%] ({label})"
        )
        st.progress(float(score))

    with st.expander("Model Notes"):
        st.write(
            "- Model: Logistic Regression with median imputation and standard scaling"
            "\n- Training data: local `data/raw/gallstone.csv`"
            "\n- Leakage variables excluded: AST, ALT, ALP, CRP"
        )


if __name__ == "__main__":
    main()
