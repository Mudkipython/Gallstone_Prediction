from gallstone_showcase.model import make_default_input, predict_risk, train_bundle


def test_model_predicts_probability() -> None:
    bundle = train_bundle(random_state=7)
    row = make_default_input(bundle)
    score = predict_risk(bundle, row)

    assert 0.0 <= score <= 1.0


def test_feature_policy_matches_notebook_track() -> None:
    bundle = train_bundle(random_state=7)

    assert "LDL_to_HDL" in bundle.feature_columns
    assert "TC_to_HDL" in bundle.feature_columns
    assert "TG_to_HDL" in bundle.feature_columns
    assert "Age_x_BMI" in bundle.feature_columns
    assert "AST_to_ALT" not in bundle.feature_columns
    assert "Aspartat Aminotransferaz (AST)" not in bundle.feature_columns
    assert "Alanin Aminotransferaz (ALT)" not in bundle.feature_columns
    assert "Alkaline Phosphatase (ALP)" not in bundle.feature_columns
    assert "C-Reactive Protein (CRP)" not in bundle.feature_columns
