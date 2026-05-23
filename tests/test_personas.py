from delphi.personas import (
    AGE_BUCKETS,
    BELIEF_AXIS,
    EDUCATION,
    INCOME_BRACKETS,
    REGIONS,
    _weighted_choice,
    sample_demographics,
)


def test_weighted_choice_returns_valid_label():
    for _ in range(50):
        choice = _weighted_choice(AGE_BUCKETS)
        assert choice in {label for label, _ in AGE_BUCKETS}


def test_sample_demographics_has_all_axes():
    d = sample_demographics()
    assert set(d.keys()) == {
        "age",
        "region",
        "education",
        "income",
        "occupation",
        "belief_axis",
    }
    assert d["age"] in {label for label, _ in AGE_BUCKETS}
    assert d["region"] in {label for label, _ in REGIONS}
    assert d["education"] in {label for label, _ in EDUCATION}
    assert d["income"] in {label for label, _ in INCOME_BRACKETS}
    assert d["belief_axis"] in {label for label, _ in BELIEF_AXIS}


def test_weights_sum_close_to_one():
    for dist in (AGE_BUCKETS, REGIONS, EDUCATION, INCOME_BRACKETS, BELIEF_AXIS):
        total = sum(w for _, w in dist)
        assert abs(total - 1.0) < 0.02, f"{dist} weights sum to {total}"


def test_regions_are_nine_census_divisions():
    expected = {
        "New England",
        "Mid-Atlantic",
        "East North Central",
        "West North Central",
        "South Atlantic",
        "East South Central",
        "West South Central",
        "Mountain",
        "Pacific",
    }
    actual = {label for label, _ in REGIONS}
    assert actual == expected
