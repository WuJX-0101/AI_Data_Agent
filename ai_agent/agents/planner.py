import json
import re
from langchain_core.messages import HumanMessage, SystemMessage


PLANNER_SYSTEM_PROMPT = """你是一个数据处理规划专家。根据用户的请求和数据信息，生成结构化的任务计划。

输出格式为 JSON 数组，每个元素包含：
- action: 操作类型 (clean/analyze/visualize/export)
- params: 操作参数

重要规则：
- 只使用下面列出的参数，不要添加任何额外参数
- 列名必须来自数据信息中的 columns 列表
- 严格遵守参数格式，不要自由发挥

支持的操作和参数（严格遵守，不要添加其他参数）：

1. clean: 数据清洗
   - remove_duplicates: bool（可选）
   - fill_missing: "mean" | "zero" | "drop"（可选）

2. analyze: 统计分析
   - group_by: string（可选，分组列名，必须是数据中已有的列）
   - metrics: array（可选，值只能是 "sum"、"mean"、"count"）

3. visualize: 可视化
   - chart_type: "bar" | "line" | "pie" | "scatter"
   - x: string（列名）
   - y: string（列名）

4. export: 导出
   - format: "xlsx" | "csv"

如果用户请求不明确，返回：{"need_clarification": true, "questions": ["问题1", "问题2"]}

示例输出：
[{"action": "analyze", "params": {"group_by": "category", "metrics": ["sum"]}}, {"action": "visualize", "params": {"chart_type": "bar", "x": "category", "y": "revenue_sum"}}]
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
        # 去掉 markdown 代码块标记
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise ValueError(f"LLM 返回了非 JSON 格式响应：{content[:200]}")
    return planner
