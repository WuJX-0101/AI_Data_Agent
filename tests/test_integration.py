import pandas as pd
import pytest
from unittest.mock import MagicMock
from ai_agent.workflow import create_workflow


def test_full_workflow():
    """端到端测试：上传文件 → 自然语言指令 → 检查输出"""
    df = pd.DataFrame({
        "cat": ["A", "A", "B", "B", "C"],
        "val": [10, 20, 30, 40, 50]
    })

    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = '[{"action": "analyze", "params": {"group_by": "cat", "metrics": ["sum"]}}]'

    workflow = create_workflow(mock_llm)
    result = workflow(df, "按类别汇总", {"columns": ["cat", "val"], "rows": 5})

    assert result["status"] == "completed"
    assert "val_sum" in result["data"].columns
    assert len(result["data"]) == 3
