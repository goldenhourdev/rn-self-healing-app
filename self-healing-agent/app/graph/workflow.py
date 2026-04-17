from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from .nodes import call_model, should_continue
from app.tools.github_tools import github_tools

class AgentState(dict):
    pass

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("action", ToolNode(github_tools))

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"action": "action", "end": END})
workflow.add_edge("action", "agent")

memory = MemorySaver()
# HITL: Pause before 'action' (writing to GitHub)
app = workflow.compile(checkpointer=memory, interrupt_before=["action"])
