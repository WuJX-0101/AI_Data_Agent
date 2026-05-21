import pandas as pd
import pytest
from ai_agent.tools.data_cleaner import clean_data


def test_remove_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = clean_data(df, remove_duplicates=True)
    assert len(result) == 2


def test_fill_missing_mean():
    df = pd.DataFrame({"a": [1, None, 3], "b": [4, 5, 6]})
    result = clean_data(df, fill_missing="mean")
    assert result["a"].iloc[1] == 2.0


def test_fill_missing_zero():
    df = pd.DataFrame({"a": [1, None, 3]})
    result = clean_data(df, fill_missing="zero")
    assert result["a"].iloc[1] == 0


def test_remove_duplicates_false():
    df = pd.DataFrame({"a": [1, 1, 2]})
    result = clean_data(df, remove_duplicates=False)
    assert len(result) == 3
