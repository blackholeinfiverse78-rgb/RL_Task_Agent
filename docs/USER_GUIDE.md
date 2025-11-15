# User Guide

## Getting Started

### 1. Launch the Demo
```bash
streamlit run demo_app.py
```
Open http://localhost:8501 in your browser.

### 2. Using the Interface

#### Task Management
- **View Tasks**: See all tasks with status filters
- **Task Details**: Toggle to show task information
- **Status Filter**: Filter by pending/in_progress/done

#### RL Agent
- **Exploration Rate**: Adjust epsilon (0.0 = exploit, 1.0 = explore)
- **Suggest Task**: Get AI-powered task recommendation
- **Rate Completion**: Provide feedback (0.0-1.0) to improve learning

#### Learning Stats
- **Tasks Learned**: Number of tasks with Q-values
- **Avg Q-Value**: Average learning score
- **Best Task**: Highest-rated task
- **Q-Table**: View raw learning data

### 3. Workflow Example

1. **Get Suggestion**
   - Click "Suggest Next Task"
   - System shows recommended task with AI reasoning

2. **Complete Task**
   - Work on the suggested task
   - Rate your completion experience (0.0-1.0)

3. **Submit Feedback**
   - Click "Submit Feedback"
   - System updates Q-learning model

4. **Repeat**
   - Get new suggestions
   - System learns from your preferences

## API Usage

### Basic Task Retrieval
```bash
curl http://localhost:8001/tasks
```

### Get Task Suggestion
```bash
curl -X POST http://localhost:8001/suggest
```

### Submit Feedback
```bash
curl -X POST http://localhost:8001/feedback/1/0.8
```

### Complete Task
```bash
curl -X POST http://localhost:8001/complete/1
```

## Configuration

### Environment Variables
```bash
# LLM Provider (choose one)
GEMINI_API_KEY=your_key
HUGGINGFACE_API_KEY=your_key
# Ollama: no key needed

# Database
USE_SQLITE=true  # Use SQLite instead of JSON

# Development
DEBUG=true
LOG_LEVEL=INFO
```

### Task Data Format
```json
{
  "task_id": 1,
  "name": "Review pull request",
  "status": "pending",
  "reward": 0.0
}
```

## Tips & Best Practices

### Effective Feedback
- **0.0-0.3**: Poor task suggestion
- **0.4-0.6**: Neutral/average
- **0.7-1.0**: Excellent suggestion

### Exploration vs Exploitation
- **High Epsilon (0.7-1.0)**: Explore new tasks
- **Low Epsilon (0.0-0.3)**: Use learned preferences
- **Balanced (0.2-0.5)**: Recommended for most use

### Learning Optimization
- Provide consistent feedback
- Rate based on task relevance and timing
- Use the system regularly for better learning