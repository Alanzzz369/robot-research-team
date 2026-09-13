from langgraph.graph import StateGraph, END
from state import ResearchState
from agents import planner_node, researcher_node, critic_node, writer_node

def route_after_critic(state):
    if state["needs_more_research"]:
        return "researcher"
    return "writer"

builder = StateGraph(ResearchState)
builder.add_node("planner", planner_node)
builder.add_node("researcher", researcher_node)
builder.add_node("critic", critic_node)
builder.add_node("writer", writer_node)

builder.set_entry_point("planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "critic")
builder.add_conditional_edges("critic", route_after_critic, {
    "researcher": "researcher",
    "writer": "writer"
})
builder.add_edge("writer", END)

graph = builder.compile()