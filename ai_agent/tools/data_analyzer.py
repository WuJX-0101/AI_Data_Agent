import pandas as pd


def analyze_data(
    df: pd.DataFrame,
    group_by: str = None,
    metrics: list[str] = None
) -> pd.DataFrame:
    """统计分析：分组聚合"""
    if not metrics:
        metrics = ["sum"]

    if group_by:
        agg_dict = {col: metrics for col in df.select_dtypes("number").columns}
        result = df.groupby(group_by).agg(agg_dict)
        result.columns = ["_".join(col) for col in result.columns]
        return result
    else:
        result = {}
        for metric in metrics:
            if metric == "sum":
                result["sum"] = df.select_dtypes("number").sum()
            elif metric == "mean":
                result["mean"] = df.select_dtypes("number").mean()
            elif metric == "count":
                result["count"] = df.select_dtypes("number").count()
        return pd.DataFrame(result)
