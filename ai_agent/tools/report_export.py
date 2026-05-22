import pandas as pd


def export_report(
    df: pd.DataFrame,
    output_path: str,
    format: str = "csv",
    charts: list = None,
    encoding: str = "utf-8-sig"
) -> str:
    """导出报告为 Excel 或 CSV"""
    if format == "csv":
        df.to_csv(output_path, index=False, encoding=encoding)
    elif format == "xlsx":
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Data")
    return output_path
