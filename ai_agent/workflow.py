import pandas as pd
from typing import TypedDict
from langgraph.graph import StateGraph, END
from ai_agent.agents.planner import create_planner
from ai_agent.agents.executor import create_executor
from ai_agent.agents.visualizer import create_visualizer


class AgentState(TypedDict):
    data: pd.DataFrame
    user_request: str
    data_info: dict
    task_plan: list
    charts: list
    status: str
    clarification_needed: bool
    clarification_questions: list


def create_workflow(llm):
    """创建 LangGraph 工作流"""
    planner = create_planner(llm)
    executor = create_executor()
    visualizer = create_visualizer()

    def plan_node(state: AgentState) -> AgentState:
        result = planner(state["user_request"], state["data_info"])
        if isinstance(result, dict) and result.get("need_clarification"):
            return {
                **state,
                "clarification_needed": True,
                "clarification_questions": result["questions"],
                "status": "awaiting_clarification"
            }
        return {**state, "task_plan": result, "clarification_needed": False, "status": "planned"}

    def execute_node(state: AgentState) -> AgentState:
        data = executor(state["data"], state["task_plan"])
        charts = visualizer(data, state["task_plan"])
        return {**state, "data": data, "charts": charts, "status": "completed"}

    def should_continue(state: AgentState) -> str:
        if state.get("clarification_needed"):
            return "end"
        return "execute"

    graph = StateGraph(AgentState)
    graph.add_node("plan", plan_node)
    graph.add_node("execute", execute_node)
    graph.set_entry_point("plan")
    graph.add_conditional_edges("plan", should_continue, {"end": END, "execute": "execute"})
    graph.add_edge("execute", END)

    compiled = graph.compile()

    def run(df: pd.DataFrame, user_request: str, data_info: dict) -> dict:
        initial_state = {
            "data": df,
            "user_request": user_request,
            "data_info": data_info,
            "task_plan": [],
            "charts": [],
            "status": "started",
            "clarification_needed": False,
            "clarification_questions": []
        }
        result = compiled.invoke(initial_state)
        return {
            "data": result["data"],
            "charts": result["charts"],
            "status": result["status"],
            "questions": result.get("clarification_questions", [])
        }

    return run
