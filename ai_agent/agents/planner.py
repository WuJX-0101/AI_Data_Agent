import json
from langchain_core.messages import HumanMessage, SystemMessage


PLANNER_SYSTEM_PROMPT = """你是一个数据处理规划专家。根据用户的请求和数据信息，生成结构化的任务计划。

输出格式为 JSON 数组，每个元素包含：
- action: 操作类型 (clean/analyze/visualize/export)
- params: 操作参数

支持的操作：
1. clean: 数据清洗
   - remove_duplicates: bool
   - fill_missing: "mean" | "zero" | "drop"
2. analyze: 统计分析
   - group_by: 分组列名
   - metrics: ["sum", "mean", "count"]
3. visualize: 可视化
   - chart_type: "bar" | "line" | "pie" | "scatter"
   - x: x轴列名
   - y: y轴列名
4. export: 导出
   - format: "xlsx" | "csv"

如果用户请求不明确，返回 JSON 格式：{"need_clarification": true, "questions": ["问题1", "问题2"]}
"""


def create_planner(llm):
    """创建 Planner Agent"""
    def planner(user_request: str, data_info: dict) -> list | dict:
        messages = [
            SystemMessage(content=PLANNER_SYSTEM_PROMPT),
            HumanMessage(content=f"用户请求: {user_request}\n数据信息: {data_info}")
        ]
        response = llm.invoke(messages)
        content = response.content.strip()
        if not content:
            raise ValueError("LLM 返回了空响应，请检查 API Key 和模型配置是否正确")
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(f"LLM 返回了非 JSON 格式响应：{content[:200]}")
    return planner
