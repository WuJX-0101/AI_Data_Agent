import pandas as pd
import plotly.graph_objects as go


def make_chart(
    df: pd.DataFrame,
    chart_type: str = "bar",
    x: str = None,
    y: str = None,
    title: str = None
) -> go.Figure:
    """生成 Plotly 图表"""
    fig = go.Figure()

    if chart_type == "bar":
        fig.add_trace(go.Bar(x=df[x], y=df[y], name=y))
    elif chart_type == "line":
        fig.add_trace(go.Scatter(x=df[x], y=df[y], mode="lines+markers", name=y))
    elif chart_type == "pie":
        fig.add_trace(go.Pie(labels=df[x], values=df[y]))
    elif chart_type == "scatter":
        fig.add_trace(go.Scatter(x=df[x], y=df[y], mode="markers", name=y))

    fig.update_layout(title=title or f"{chart_type} chart")
    return fig
