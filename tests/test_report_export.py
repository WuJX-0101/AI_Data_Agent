import pandas as pd
import os
import pytest
from ai_agent.tools.report_export import export_report


def test_export_excel(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    output_path = tmp_path / "report.xlsx"
    export_report(df, str(output_path), format="xlsx")
    assert os.path.exists(output_path)


def test_export_csv(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    output_path = tmp_path / "report.csv"
    export_report(df, str(output_path), format="csv")
    assert os.path.exists(output_path)


def test_export_with_charts(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    output_path = tmp_path / "report.xlsx"
    export_report(df, str(output_path), format="xlsx", charts=[])
    assert os.path.exists(output_path)
