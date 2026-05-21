import pandas as pd
import pytest
from ai_agent.agents.executor import create_executor


def test_executor_clean():
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    executor = create_executor()
    plan = [{"action": "clean", "params": {"remove_duplicates": True}}]
    result = executor(df, plan)
    assert len(result) == 2


def test_executor_analyze():
    df = pd.DataFrame({"cat": ["a", "a", "b"], "val": [1, 2, 3]})
    executor = create_executor()
    plan = [{"action": "analyze", "params": {"group_by": "cat", "metrics": ["sum"]}}]
    result = executor(df, plan)
    assert "val_sum" in result.columns
