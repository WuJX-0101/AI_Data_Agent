import pandas as pd


def clean_data(
    df: pd.DataFrame,
    remove_duplicates: bool = False,
    fill_missing: str = None
) -> pd.DataFrame:
    """清洗数据：去重、填充缺失值"""
    result = df.copy()

    if remove_duplicates:
        result = result.drop_duplicates()

    if fill_missing:
        if fill_missing == "mean":
            result = result.fillna(result.mean(numeric_only=True))
        elif fill_missing == "zero":
            result = result.fillna(0)
        elif fill_missing == "drop":
            result = result.dropna()

    return result
