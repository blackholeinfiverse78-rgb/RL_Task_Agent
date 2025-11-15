# Run Commands

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Main Applications
```bash
# Streamlit Demo UI
streamlit run demo_app.py

# Production API
python app.py
```

## Testing
```bash
# Test all components
python tests/test_components.py

# Run 6-step workflow demo
python tests/workflow_demo.py

# Run learning simulation
python tests/simulation_test.py
```

## Utilities
```bash
# Reset project data
python scripts/util_scripts.py reset

# Add sample tasks
python scripts/util_scripts.py sample

# Show project status
python scripts/util_scripts.py status

# Generate flow diagram
python scripts/create_flow_diagram.py
```

## Environment Setup
```bash
# Set OpenAI API key
export OPENAI_API_KEY="your_key_here"

# Or use HuggingFace
export HUGGINGFACE_API_KEY="your_key_here"

# Use SQLite database
export USE_SQLITE=true
```

## Project Structure
```
RL_TASK_AGENT/
├── app.py                    # Production API
├── demo_app.py               # Streamlit demo UI
├── task_agent/               # Core modules
├── docs/                     # Documentation
├── tests/                    # Test files
└── scripts/                  # Utility scripts
```