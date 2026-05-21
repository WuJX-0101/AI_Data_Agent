import pandas as pd
import plotly.graph_objects as go
import pytest
from ai_agent.tools.chart_maker import make_chart


def test_bar_chart():
    df = pd.DataFrame({"x": ["a", "b", "c"], "y": [1, 2, 3]})
    fig = make_chart(df, chart_type="bar", x="x", y="y")
    assert isinstance(fig, go.Figure)


def test_line_chart():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
    fig = make_chart(df, chart_type="line", x="x", y="y")
    assert isinstance(fig, go.Figure)


def test_pie_chart():
    df = pd.DataFrame({"labels": ["a", "b"], "values": [3, 7]})
    fig = make_chart(df, chart_type="pie", x="labels", y="values")
    assert isinstance(fig, go.Figure)
