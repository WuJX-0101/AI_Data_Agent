import pandas as pd
from ai_agent.tools.data_cleaner import clean_data
from ai_agent.tools.data_analyzer import analyze_data


def create_executor():
    """创建 Executor Agent"""
    def executor(df: pd.DataFrame, plan: list) -> pd.DataFrame:
        result = df.copy()
        for step in plan:
            action = step["action"]
            params = step.get("params", {})
            if action == "clean":
                result = clean_data(result, **params)
            elif action == "analyze":
                result = analyze_data(result, **params)
        return result
    return executor
