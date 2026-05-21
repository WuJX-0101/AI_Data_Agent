import pandas as pd
from ai_agent.tools.chart_maker import make_chart


def create_visualizer():
    """创建 Visualizer Agent"""
    def visualizer(df: pd.DataFrame, plan: list) -> list:
        charts = []
        for step in plan:
            if step["action"] == "visualize":
                params = step.get("params", {})
                fig = make_chart(df, **params)
                charts.append(fig)
        return charts
    return visualizer
