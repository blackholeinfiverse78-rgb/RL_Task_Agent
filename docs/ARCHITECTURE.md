# System Architecture

## Overview
RL Task Agent combines Reinforcement Learning with Large Language Models for intelligent task management.

## Architecture Diagram
```
┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │    │   FastAPI REST  │
│   (demo_app.py) │    │     (app.py)    │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          └──────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    LangChain Agent    │
         │ (langchain_agent.py)  │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐    ┌───────▼───────┐    ┌───▼───┐
│Gemini │    │  HuggingFace  │    │Ollama │
│ (API) │    │     (API)     │    │(Local)│
└───────┘    └───────────────┘    └───────┘
                     │
         ┌───────────▼───────────┐
         │      RL Model         │
         │    (rl_model.py)      │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼───┐    ┌───────▼───────┐    ┌───▼───┐
│ JSON  │    │    SQLite     │    │Memory │
│Files  │    │  (database.py)│    │ JSON  │
└───────┘    └───────────────┘    └───────┘
```

## Components

### 1. Frontend Layer
- **Streamlit UI**: Interactive demo interface
- **FastAPI REST**: Production API endpoints

### 2. Agent Layer
- **LangChain Agent**: Multi-LLM orchestration
- **LLM Providers**: Gemini → HuggingFace → Ollama fallback

### 3. Learning Layer
- **RL Model**: Q-learning algorithm
- **Memory**: Persistent Q-table storage

### 4. Data Layer
- **JSON Files**: Simple file-based storage
- **SQLite**: Relational database option
- **Agent Memory**: Q-value persistence

## Data Flow

1. **Task Input** → System loads tasks from JSON/SQLite
2. **RL Selection** → Q-learning chooses optimal task
3. **LLM Reasoning** → Multi-LLM provides explanation
4. **User Feedback** → Reward updates Q-table
5. **Learning** → System improves over time

## Key Features

### Multi-LLM Support
- **Primary**: Gemini (best performance)
- **Fallback**: HuggingFace (cost-effective)
- **Local**: Ollama (privacy-focused)
- **Final**: RL-only (no external dependencies)

### Adaptive Learning
- Q-learning algorithm learns from user feedback
- Epsilon-greedy exploration vs exploitation
- Persistent memory across sessions

### Flexible Storage
- JSON files for simplicity
- SQLite for production scalability
- Automatic migration between formats