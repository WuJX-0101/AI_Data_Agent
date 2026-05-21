import pandas as pd
import pytest
from unittest.mock import MagicMock
from ai_agent.workflow import create_workflow


def test_workflow_returns_result():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = '[{"action": "clean", "params": {"remove_duplicates": true}}]'
    workflow = create_workflow(mock_llm)
    df = pd.DataFrame({"a": [1, 1, 2]})
    result = workflow(df, "清理重复数据", {"columns": ["a"], "rows": 3})
    assert len(result["data"]) == 2
    assert result["status"] == "completed"
