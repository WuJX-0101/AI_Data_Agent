import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# 从项目根目录的 .env 加载
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_llm(model_name: str = None):
    """根据模型名称返回对应的 LLM 实例"""
    model = model_name or os.getenv("DEFAULT_MODEL", "gpt-4o")

    if model.startswith("gpt"):
        return ChatOpenAI(model=model, api_key=os.getenv("OPENAI_API_KEY"))
    elif model.startswith("claude"):
        return ChatAnthropic(model=model, api_key=os.getenv("ANTHROPIC_API_KEY"))
    elif model.startswith("deepseek"):
        return ChatOpenAI(
            model=model,
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
    else:
        raise ValueError(f"不支持的模型: {model}")


AVAILABLE_MODELS = [
    {"name": "deepseek-v4-flash", "provider": "DeepSeek"},
    {"name": "deepseek-v4-pro", "provider": "DeepSeek"},
    {"name": "gpt-4o", "provider": "OpenAI"},
    {"name": "gpt-4o-mini", "provider": "OpenAI"},
    {"name": "claude-sonnet-4-20250514", "provider": "Anthropic"},
    {"name": "claude-haiku-4-5-20251001", "provider": "Anthropic"},

]
