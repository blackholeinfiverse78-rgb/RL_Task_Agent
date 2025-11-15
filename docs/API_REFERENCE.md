# API Reference

## Base URL
```
http://127.0.0.1:8001
```

## Endpoints

### GET /
**System Status & Configuration**
```json
{
  "message": "RL Task Agent API",
  "version": "2.0.0",
  "endpoints": [...],
  "features": {
    "sqlite": false,
    "langchain": true,
    "gemini": true,
    "active_llm": "gemini"
  }
}
```

### GET /tasks
**Get All Tasks**
```json
{
  "tasks": [
    {
      "task_id": 1,
      "name": "Review code",
      "status": "pending"
    }
  ],
  "count": 1
}
```

### GET /tasks/{status}
**Get Tasks by Status**
- Parameters: `status` (pending, in_progress, done)

### POST /suggest
**Get Task Suggestion**
```json
{
  "task": {
    "task_id": 1,
    "name": "Review code"
  },
  "reasoning": "AI explanation",
  "llm_provider": "gemini",
  "q_value": 0.75
}
```

### POST /feedback/{task_id}/{reward}
**Submit Task Feedback**
- Parameters: `task_id` (int), `reward` (0.0-1.0)

### POST /complete/{task_id}
**Mark Task Complete**
- Parameters: `task_id` (int)

### GET /stats
**System Statistics**
```json
{
  "rl_stats": {
    "total_tasks": 5,
    "avg_q_value": 0.45,
    "best_task_id": "3"
  },
  "q_table": {...},
  "llm_status": {...}
}
```