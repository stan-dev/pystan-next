"""Test building a Stan program."""
import pytest

import stan


def test_build_basic():
    program_code = "parameters {real y;} model {y ~ normal(0,1);}"
    posterior = stan.build(program_code)
    assert posterior.model_name is not None
    assert posterior.data == {}
    assert posterior.param_names == ("y",)


def test_stanc_no_such_distribution():
    program_code = "parameters {real z;} model {z ~ no_such_distribution();}"
    with pytest.raises(ValueError, match=r"Semantic error"):
        stan.build(program_code=program_code)


def test_stanc_invalid_assignment():
    program_code = "parameters {real z;} model {z = 3;}"
    with pytest.raises(ValueError, match=r"Semantic error"):
        stan.build(program_code=program_code)


def test_stanc_exception_semicolon():
    program_code = """
    parameters {
        real z
        real y
    }
    model {
        z ~ normal(0, 1);
        y ~ normal(0, 1);}
    """
    with pytest.raises(ValueError, match=r"Syntax error"):
        stan.build(program_code=program_code)
