# AI 数据处理助手

基于 LangGraph + Streamlit 的多智能体数据处理工具，支持自然语言驱动的数据清洗、分析、可视化和报告导出。

## 功能

- **数据清洗**：去重、缺失值填充、筛选过滤
- **统计分析**：分组聚合（sum/mean/count）
- **数据可视化**：柱状图、折线图、饼图（Plotly）
- **报告导出**：CSV（支持 UTF-8/GBK 编码）和 XLSX 格式
- **多模型支持**：OpenAI GPT-4o、Anthropic Claude、DeepSeek

## 架构

```
用户输入 → Planner（规划） → Executor（执行） → Visualizer（可视化）
                ↓                   ↓
           任务分解            数据清洗/分析/导出
```

- `ai_agent/workflow.py` — LangGraph 工作流编排
- `ai_agent/agents/` — Planner、Executor、Visualizer 智能体
- `ai_agent/tools/` — 数据清洗、分析、图表、导出工具
- `ai_agent/app.py` — Streamlit UI

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入对应的 API Key：

```bash
cp .env.example .env
```

```env
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
```

### 3. 启动

```bash
streamlit run ai_agent/app.py
```

## 支持的模型

| 模型 | 提供商 |
|------|--------|
| deepseek-v4-flash | DeepSeek |
| deepseek-v4-pro | DeepSeek |
| gpt-4o | OpenAI |
| gpt-4o-mini | OpenAI |
| claude-sonnet-4-20250514 | Anthropic |
| claude-haiku-4-5-20251001 | Anthropic |

## 测试

```bash
python -m pytest tests/
```

## 技术栈

- Python 3.10+
- LangGraph / LangChain
- Streamlit
- Pandas / Openpyxl
- Plotly
