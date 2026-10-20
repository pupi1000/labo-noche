from langchain_core.messages import SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from .config import Settings
from .prompts import SYSTEM_PROMPT
from .providers import build_chat_model
from .tool_registry import get_domain_tools


def build_graph(provider: str, settings: Settings | None = None):
    s = settings or Settings()
    model = build_chat_model(provider, s)
    domain_tools = get_domain_tools(s.enable_student_extension)
    tools = [
        StructuredTool.from_function(
            fn,
            name=fn.__name__,
            description=(fn.__doc__ or fn.__name__).strip(),
        )
        for fn in domain_tools
    ]
    bound = model.bind_tools(tools)

    def agent_node(state: MessagesState):
        messages = state["messages"]
        if not messages or getattr(messages[0], "type", "") != "system":
            messages = [SystemMessage(content=SYSTEM_PROMPT), *messages]
        response = bound.invoke(messages)
        return {"messages": [response]}

    def route(state: MessagesState):
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else END

    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools, handle_tool_errors=True))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", route, {"tools": "tools", END: END})
    builder.add_edge("tools", "agent")
    return builder.compile()


def safe_message_payload(message) -> dict:
    payload = {"type": getattr(message, "type", message.__class__.__name__)}
    content = getattr(message, "content", "")
    if isinstance(content, str) and content:
        payload["content"] = content
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        payload["tool_calls"] = [
            {"name": x.get("name"), "args": x.get("args", {})} for x in tool_calls
        ]
    if payload["type"] == "tool":
        payload["tool_name"] = getattr(message, "name", None)
    return payload
