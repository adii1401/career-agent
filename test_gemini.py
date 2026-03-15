import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool

load_dotenv()

@tool
def test_tool(query: str) -> str:
    """A simple test tool that returns the query."""
    return f"Tool called with: {query}"

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools([test_tool])

result = llm_with_tools.invoke("Use the test tool with query 'hello'")
print(result)
print("Tool calls:", result.tool_calls)