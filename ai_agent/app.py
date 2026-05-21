import streamlit as st
import pandas as pd
from config import get_llm, AVAILABLE_MODELS
from ai_agent.workflow import create_workflow


st.set_page_config(page_title="AI 数据处理助手", layout="wide")
st.title("AI 数据处理助手")

# 侧边栏设置
with st.sidebar:
    st.header("设置")
    selected_model = st.selectbox("选择模型", [m["name"] for m in AVAILABLE_MODELS])
    api_key = st.text_input("API Key", type="password")
    st.session_state["model"] = selected_model
    st.session_state["api_key"] = api_key

# 文件上传
uploaded_file = st.file_uploader("上传数据文件", type=["xlsx", "csv", "json"])

if uploaded_file:
    # 读取文件
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
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

                    if result["status"] == "awaiting_clarification":
                        st.info("需要更多信息：")
                        for q in result["questions"]:
                            st.write(f"- {q}")
                    else:
                        st.success("处理完成！")
                        st.subheader("处理结果")
                        st.dataframe(result["data"])

                        if result["charts"]:
                            st.subheader("图表")
                            for chart in result["charts"]:
                                st.plotly_chart(chart)

                        # 下载按钮
                        if export:
                            csv = result["data"].to_csv(index=False)
                            st.download_button("下载 CSV", csv, "report.csv", "text/csv")
                except Exception as e:
                    st.error(f"处理失败: {str(e)}")
