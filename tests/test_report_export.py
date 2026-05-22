import pandas as pd
import io
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


def test_export_csv_chinese(tmp_path):
    df = pd.DataFrame({"类别": ["服装", "电子产品", "食品"], "销售额": [100, 200, 300]})
    output_path = tmp_path / "report_cn.csv"
    export_report(df, str(output_path), format="csv")
    with open(output_path, "rb") as f:
        raw = f.read()
    # UTF-8 with BOM: EF BB BF
    assert raw[:3] == b"\xef\xbb\xbf", "CSV should have UTF-8 BOM for Windows Excel compatibility"
    content = raw[3:].decode("utf-8")
    assert "服装" in content
    assert "电子产品" in content
    assert "食品" in content


def test_export_with_charts(tmp_path):
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    output_path = tmp_path / "report.xlsx"
    export_report(df, str(output_path), format="xlsx", charts=[])
    assert os.path.exists(output_path)


def test_gbk_read_then_export(tmp_path):
    """GBK CSV 读取后导出，中文完整保留"""
    # 创建 GBK 编码的 CSV
    original = pd.DataFrame({"类别": ["服装", "电子产品", "食品"], "销售额": [100, 200, 300]})
    gbk_path = tmp_path / "input.csv"
    original.to_csv(gbk_path, index=False, encoding="gbk")

    # 模拟 app.py 的读取逻辑
    with open(gbk_path, "rb") as f:
        content = f.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("gbk")
    df = pd.read_csv(io.StringIO(text))

    # 导出为 CSV
    output_path = tmp_path / "output.csv"
    export_report(df, str(output_path), format="csv")

    # 验证导出内容
    with open(output_path, "rb") as f:
        raw = f.read()
    decoded = raw[3:].decode("utf-8")  # 跳过 BOM
    assert "服装" in decoded
    assert "电子产品" in decoded
    assert "食品" in decoded
