# Agent-using-LangChain

## LangChain Agent System (Multi-Model + Tool-Based)

## Overview
This project implements a **LangChain-based AI Agent** that combines:
- Multiple LLMs (local + cloud)
- Tool usage (calculator, search)
- Dynamic decision-making using middleware

The agent follows the **ReAct (Reasoning + Acting)** paradigm to:
- Understand user queries  
- Decide whether to use tools  
- Execute actions  
- Return final responses  

---

## Features

### 1. Multi-Model Support
- **Basic Model (Local)**: Granite 3.2 (8B) via Ollama  
- **Advanced Model (Cloud)**: Google Gemini API  

The system dynamically switches between models based on conversation complexity.

---

### 2. Dynamic Model Selection
- Implemented using LangChain middleware (`@wrap_model_call`)
- Logic:
  - Short/simple conversations → Local model  
  - Longer/complex conversations → Gemini  

---

### 3. Tool Integration

#### Available Tools:
- **Public Search** → General queries  
- **Private Search** → Restricted/internal queries  
- **Calculator** → Evaluates mathematical expressions  

---

### 4. Dynamic Tool Filtering
- Tools are filtered based on conversation state:
  - Early stage → limited tools  
  - Later stage → full access  

---

### 5. Tool Error Handling
- Implemented using `@wrap_tool_call`
- Prevents crashes during tool execution  
- Returns meaningful error messages  

---

### 6. ReAct Agent Loop
The agent follows the ReAct loop:
1. Reason about the problem  
2. Decide tool usage  
3. Execute tool  
4. Observe result  
5. Repeat until final answer  

---

### 7. System Prompt
Defines agent behavior:
> "You are a smart AI assistant. Use tools when necessary."

---

## Architecture

User Input  
↓  
Agent (create_agent)  
↓  
Middleware Layer  
├── Dynamic Model Selection  
├── Dynamic Tool Filtering  
└── Tool Error Handling  
↓  
Model (LLM)  
↓  
Tool Execution (if required)  
↓  
Final Response

---

## Tech Stack
- Python  
- LangChain  
- Ollama (Granite 3.2 8B)  
- Google Gemini API  
- python-dotenv  

---

## Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```bash
GEMINI_API_KEY=your_api_key_here
```

---

## Running the Project

```bash
python agent.py
```

---

## Example Usage

```
You: What is 25 * 8?
Agent: 200

You: Search latest AI trends
Agent: [Public Search] Results for: latest AI trends
```

---

## Known Limitations
- Calculator uses `eval()` (not safe for production)
- Search tool is mocked
- Ollama has limited tool-calling support
- Streaming was tested but not included due to instability

---

## Key Concepts Demonstrated
- LangChain `create_agent`
- Middleware-based architecture
- Dynamic model routing
- Dynamic tool availability
- Tool error handling
- ReAct reasoning loop

---

## Conclusion

This project demonstrates a modular AI agent system capable of:

- Multi-model reasoning
- Tool-based execution
- Adaptive decision-making
