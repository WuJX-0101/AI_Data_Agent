import pandas as pd
import pytest
from ai_agent.tools.data_analyzer import analyze_data


def test_group_sum():
    df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [1, 2, 3]})
    result = analyze_data(df, group_by="cat", metrics=["sum"])
    assert result.loc["a", "val_sum"] == 3
    assert result.loc["b", "val_sum"] == 3


def test_group_mean():
    df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [1, 3, 5]})
    result = analyze_data(df, group_by="cat", metrics=["mean"])
    assert result.loc["a", "val_mean"] == 2.0
    assert result.loc["b", "val_mean"] == 5.0


def test_no_group():
    df = pd.DataFrame({"val": [1, 2, 3]})
    result = analyze_data(df, metrics=["sum"])
    assert result.loc["val", "sum"] == 6
