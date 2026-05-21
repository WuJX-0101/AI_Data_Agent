import pandas as pd
import plotly.graph_objects as go
import pytest
from ai_agent.agents.visualizer import create_visualizer


def test_visualizer_creates_chart():
    df = pd.DataFrame({"x": ["a", "b", "c"], "y": [1, 2, 3]})
    visualizer = create_visualizer()
    plan = [{"action": "visualize", "params": {"chart_type": "bar", "x": "x", "y": "y"}}]
    charts = visualizer(df, plan)
    assert len(charts) == 1
    assert isinstance(charts[0], go.Figure)


def test_visualizer_multiple_charts():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6], "z": [7, 8, 9]})
    visualizer = create_visualizer()
    plan = [
        {"action": "visualize", "params": {"chart_type": "line", "x": "x", "y": "y"}},
        {"action": "visualize", "params": {"chart_type": "scatter", "x": "x", "y": "z"}}
    ]
    charts = visualizer(df, plan)
    assert len(charts) == 2
