# Installation Guide

## Prerequisites
- Python 3.8+
- pip package manager

## Quick Setup

### 1. Clone & Install
```bash
git clone <repository-url>
cd rl_task_agent
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
GEMINI_API_KEY=your_gemini_key_here
# OR
HUGGINGFACE_API_KEY=your_hf_key_here
# OR use Ollama (no key needed)
```

### 3. Database Setup (Optional)
```bash
# Use SQLite instead of JSON
echo "USE_SQLITE=true" >> .env
```

### 4. Start Applications
```bash
# Demo UI
streamlit run demo_app.py

# Production API
python app.py
```

## LLM Provider Setup

### Option 1: Gemini (Recommended)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set `GEMINI_API_KEY=your_key` in `.env`

### Option 2: HuggingFace
1. Get API key from [HuggingFace](https://huggingface.co/settings/tokens)
2. Set `HUGGINGFACE_API_KEY=your_key` in `.env`

### Option 3: Ollama (Local)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start server
ollama serve

# Pull model
ollama pull llama3
```

## Verification
```bash
# Test components
python tests/test_components.py

# Run workflow demo
python tests/workflow_demo.py
```