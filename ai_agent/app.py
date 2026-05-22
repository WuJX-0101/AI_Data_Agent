import io
import streamlit as st
import pandas as pd
from ai_agent.config import get_llm, AVAILABLE_MODELS
from ai_agent.workflow import create_workflow


st.set_page_config(page_title="AI 数据处理助手", layout="wide")
st.title("AI 数据处理助手")

# 侧边栏设置
with st.sidebar:
    st.header("设置")
    selected_model = st.selectbox("选择模型", [m["name"] for m in AVAILABLE_MODELS])
    st.session_state["model"] = selected_model

# 文件上传
uploaded_file = st.file_uploader("上传数据文件", type=["xlsx", "csv", "json"])

ENCODING_OPTIONS = {
    "UTF-8 (BOM)": "utf-8-sig",
    "UTF-8": "utf-8",
    "GBK": "gbk",
}


def display_result(result, export=False, encoding="utf-8-sig", file_format="csv"):
    """渲染处理结果"""
    if result["status"] == "awaiting_clarification":
        st.info("需要更多信息：")
        for q in result["questions"]:
            st.write(f"- {q}")
    elif result["status"] == "error":
        st.error(result.get("error_message", "执行出错"))
    else:
        st.success("处理完成！")
        st.subheader("处理结果")
        st.dataframe(result["data"])

        if result["charts"]:
            st.subheader("图表")
            for chart in result["charts"]:
                st.plotly_chart(chart)

        if export:
            buf = io.BytesIO()
            if file_format == "xlsx":
                with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                    result["data"].to_excel(writer, index=False, sheet_name="Data")
                st.download_button(
                    "下载 XLSX", buf.getvalue(), "report.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
            else:
                result["data"].to_csv(buf, index=False, encoding=encoding)
                st.download_button("下载 CSV", buf.getvalue(), "report.csv", "text/csv")


if uploaded_file:
    # 读取文件
    if uploaded_file.name.endswith(".csv"):
        content = uploaded_file.read()
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("gbk")
        df = pd.read_csv(io.StringIO(text))
    elif uploaded_file.name.endswith(".json"):
        df = pd.read_json(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["data"] = df

    # 数据预览
    st.subheader("数据预览")
    st.dataframe(df.head(10))

    # 操作选择
    st.subheader("选择操作")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        clean = st.checkbox("清洗筛选")
    with col2:
        analyze = st.checkbox("统计分析")
    with col3:
        visualize = st.checkbox("可视化")
    with col4:
        export = st.checkbox("导出报告")

    if export:
        col_fmt, col_enc = st.columns(2)
        with col_fmt:
            export_format = st.selectbox("下载格式", ["csv", "xlsx"], key="export_format")
        if export_format == "csv":
            with col_enc:
                encoding_label = st.selectbox("编码格式", list(ENCODING_OPTIONS.keys()), key="csv_encoding")
            export_encoding = ENCODING_OPTIONS[encoding_label]
        else:
            export_encoding = "utf-8-sig"
    else:
        export_encoding = "utf-8-sig"
        export_format = "csv"

    # 自然语言输入
    user_request = st.text_area("描述您想做的操作", placeholder="例如：按类别汇总销售额，生成柱状图")

    # 执行按钮
    if st.button("开始处理"):
        if not user_request:
            st.warning("请描述您想做的操作")
        else:
            with st.spinner("处理中..."):
                try:
                    llm = get_llm(st.session_state.get("model"))
                    workflow = create_workflow(llm)
                    data_info = {
                        "columns": list(df.columns),
                        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
                        "rows": len(df)
                    }
                    result = workflow(df, user_request, data_info)
                    st.session_state["result"] = result
                    display_result(result, export, export_encoding, export_format)
                except Exception as e:
                    st.error(f"处理失败: {str(e)}")
    elif "result" in st.session_state:
        display_result(st.session_state["result"], export, export_encoding, export_format)
