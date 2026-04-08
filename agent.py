import os
from dotenv import load_dotenv
from typing import Callable

# LangChain
from langchain.agents import create_agent
from langchain.tools import tool

# Middleware
from langchain.agents.middleware import (
    wrap_model_call,
    wrap_tool_call,
    ModelRequest,
    ModelResponse
)

# Models
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

# Messages
from langchain.messages import ToolMessage


# ENV
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# MODELS
basic_model = ChatOllama(
    model="granite3.2:8b",
    temperature=0.7
)

advanced_model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)


# DYNAMIC MODEL
@wrap_model_call
def dynamic_model(request: ModelRequest, handler) -> ModelResponse:
    """
    Switch model based on conversation complexity
    """
    message_count = len(request.state["messages"])

    if message_count > 5:
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))


# TOOLS (STATIC)
@tool
def public_search(query: str) -> str:
    """Search public information"""
    return f"[Public Search] Results for: {query}"


@tool
def private_search(query: str) -> str:
    """Search private data (restricted)"""
    return f"[Private Search] Confidential results for: {query}"


@tool
def calculator(expression: str) -> str:
    """Evaluate math expressions"""
    try:
        return str(eval(expression))
    except Exception as e:
        raise ValueError(str(e))


# DYNAMIC TOOL FILTERING
@wrap_model_call
def dynamic_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """
    Filter tools based on state
    """
    state = request.state
    message_count = len(state["messages"])

    # Example: early conversation → limit tools
    if message_count < 3:
        tools = [t for t in request.tools if t.name != "private_search"]
        request = request.override(tools=tools)

    return handler(request)


# TOOL ERROR HANDLING
@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"Tool error: {str(e)}",
            tool_call_id=request.tool_call["id"]
        )


# AGENT
agent = create_agent(
    model=basic_model,  # default
    tools=[public_search, private_search, calculator],
    system_prompt="You are a smart AI assistant. Use tools when necessary.",
    middleware=[
        dynamic_model,
        dynamic_tools,
        handle_tool_errors
    ]
)


# RUN
if __name__ == "__main__":
    print("LangChain Agent (Docs Implementation)\nType 'exit' to quit\n")

    messages = []

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        messages.append({"role": "user", "content": user_input})

        response = agent.invoke({"messages": messages})

        output = response["messages"][-1].content
        print(f"Agent: {output}")

        messages.append({"role": "assistant", "content": output})