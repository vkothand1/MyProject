"""
Sample LangChain + LangGraph script (no external API calls).

What it tests:
- LangChain prompt formatting via LangChain Core runnables
- LangGraph execution by compiling and invoking a tiny StateGraph
"""

from __future__ import annotations

import importlib.metadata
from typing import TypedDict

from langchain_core.prompts import PromptTemplate
from langgraph.graph import END, StateGraph


class GraphState(TypedDict):
    name: str
    greeting: str


def main() -> None:
    # Print installed versions so you know you're running the venv you set up.
    langchain_version = importlib.metadata.version("langchain")
    langgraph_version = importlib.metadata.version("langgraph")
    print(f"Using langchain=={langchain_version}")
    print(f"Using langgraph=={langgraph_version}")

    # LangChain: create a simple runnable chain (prompt formatting only).
    prompt = PromptTemplate.from_template("Write a friendly greeting for {name}.")

    # LangGraph: wrap the chain in a tiny graph node.
    def make_greeting(state: GraphState) -> dict:
        # `PromptTemplate.invoke(...)` returns a PromptValue (e.g. `StringPromptValue`),
        # so convert it to raw text before continuing.
        greeting_text = prompt.invoke({"name": state["name"]}).to_string()
        return {"greeting": greeting_text}

    graph = StateGraph(GraphState)
    graph.add_node("make_greeting", make_greeting)
    graph.set_entry_point("make_greeting")
    graph.add_edge("make_greeting", END)

    app = graph.compile()
    result = app.invoke({"name": "Vinoth"})

    print("Graph result:", result)


if __name__ == "__main__":
    main()

