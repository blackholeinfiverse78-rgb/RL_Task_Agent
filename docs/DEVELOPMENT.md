# Development Guide

## Project Structure
```
rl_task_agent/
├── app.py                 # FastAPI production server
├── demo_app.py           # Streamlit demo interface
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
│
├── task_agent/          # Core package
│   ├── __init__.py
│   ├── rl_model.py      # Q-learning implementation
│   ├── langchain_agent.py # Multi-LLM integration
│   ├── database.py      # SQLite operations
│   └── data/           # Data storage
│       ├── tasks.json   # Task database
│       ├── tasks.db     # SQLite database
│       └── agent_memory.json # Q-table persistence
│
├── docs/               # Documentation
├── tests/              # Test suite
└── scripts/            # Utility scripts
```

## Core Components

### 1. RL Model (`rl_model.py`)
```python
class RLModel:
    def __init__(self, memory_path="task_agent/data/agent_memory.json")
    def choose_action(self, state, tasks, epsilon=0.2)
    def update_q_value(self, task_id, reward)
    def get_task_statistics(self)
```

### 2. LangChain Agent (`langchain_agent.py`)
```python
class LangChainTaskAgent:
    def __init__(self)
    def suggest_task_with_reasoning(self, tasks)
    def _get_llm_provider(self)
```

### 3. Database (`database.py`)
```python
class TaskDatabase:
    def get_all_tasks(self)
    def update_task_status(self, task_id, status)
    def migrate_from_json(self)
```

## Adding New Features

### New LLM Provider
1. Add provider detection in `langchain_agent.py`
2. Update fallback chain in `_get_llm_provider()`
3. Add environment variable handling

### New API Endpoint
1. Add route in `app.py`
2. Update endpoint list in home()
3. Add tests in `tests/`

### New RL Algorithm
1. Extend `RLModel` class
2. Implement new learning methods
3. Update statistics calculation

## Testing

### Run All Tests
```bash
python tests/test_components.py
```

### Component Testing
```bash
# Test RL model
python -c "from task_agent.rl_model import RLModel; rl = RLModel(); print('RL OK')"

# Test LangChain
python -c "from task_agent.langchain_agent import LangChainTaskAgent; agent = LangChainTaskAgent(); print('LangChain OK')"

# Test Database
python -c "from task_agent.database import TaskDatabase; db = TaskDatabase(); print('DB OK')"
```

### Workflow Testing
```bash
python tests/workflow_demo.py
```

## Debugging

### Common Issues

#### Port Already in Use
- App automatically finds free port (8001-8100)
- Check with `netstat -an | findstr :8001`

#### LLM Provider Errors
- Check API keys in `.env`
- Verify provider availability at `/` endpoint
- System falls back to next available provider

#### Database Issues
- Check file permissions in `task_agent/data/`
- Use `USE_SQLITE=false` to disable SQLite
- Delete `.db` files to reset database

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Code Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to public methods

### Pull Request Process
1. Fork repository
2. Create feature branch
3. Add tests for new functionality
4. Update documentation
5. Submit pull request

### Environment Setup
```bash
# Development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Code formatting
black .

# Linting
flake8 .
```