import json
import pytest
from unittest.mock import MagicMock
from ai_agent.agents.planner import create_planner


def test_planner_returns_plan():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = json.dumps([
        {"action": "clean", "params": {"remove_duplicates": True}},
        {"action": "analyze", "params": {"group_by": "cat", "metrics": ["sum"]}}
    ])
    planner = create_planner(mock_llm)
    result = planner("清理数据并按类别汇总", {"columns": ["cat", "val"], "rows": 100})
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["action"] == "clean"
