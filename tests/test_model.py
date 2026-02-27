from gallstone_showcase.model import make_default_input, predict_risk, train_bundle


def test_model_predicts_probability() -> None:
    bundle = train_bundle(random_state=7)
    row = make_default_input(bundle)
    score = predict_risk(bundle, row)

    assert 0.0 <= score <= 1.0
