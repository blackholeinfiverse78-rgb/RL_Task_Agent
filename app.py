from fastapi import FastAPI, HTTPException
from task_agent.rl_model import RLModel
from task_agent.langchain_agent import LangChainTaskAgent
from task_agent.database import TaskDatabase
import json
import os
from pathlib import Path

# Load environment variables from .env file
def load_env():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()  # Load environment variables

app = FastAPI(title="RL Task Agent API", version="2.0.0")

# Initialize components
rl = RLModel()
langchain_agent = LangChainTaskAgent()
use_sqlite = os.getenv("USE_SQLITE", "false").lower() == "true"

if use_sqlite:
    db = TaskDatabase()
    db.migrate_from_json()

def detect_llm_capabilities():
    """Detect available LLM providers"""
    gemini_key = os.getenv("GEMINI_API_KEY")
    hf_key = os.getenv("HUGGINGFACE_API_KEY")
    
    return {
        "gemini": gemini_key is not None and gemini_key != "your_gemini_api_key_here",
        "huggingface": hf_key is not None and hf_key != "your_huggingface_api_key_here",
        "ollama": langchain_agent.llm_type == "ollama",
        "active_llm": langchain_agent.llm_type,
        "env_loaded": True
    }

@app.get("/")
def home():
    llm_status = detect_llm_capabilities()
    return {
        "message": "RL Task Agent API",
        "version": "2.0.0",
        "endpoints": ["/tasks", "/tasks/{status}", "/suggest", "/feedback/{task_id}/{reward}", "/complete/{task_id}", "/stats"],
        "features": {
            "sqlite": use_sqlite,
            "langchain": langchain_agent.llm is not None,
            **llm_status
        }
    }

@app.get("/tasks")
def get_tasks():
    """Get all tasks"""
    try:
        if use_sqlite:
            tasks = db.get_all_tasks()
        else:
            with open("task_agent/data/tasks.json", "r") as f:
                tasks = json.load(f)
        return {"tasks": tasks, "count": len(tasks)}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Tasks not found")

@app.get("/tasks/{status}")
def get_tasks_by_status(status: str):
    """Get tasks by status"""
    try:
        if use_sqlite:
            tasks = db.get_tasks_by_status(status)
        else:
            with open("task_agent/data/tasks.json", "r") as f:
                all_tasks = json.load(f)
            tasks = [t for t in all_tasks if t.get('status') == status]
        return {"tasks": tasks, "count": len(tasks), "status": status}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Tasks not found")

@app.post("/suggest")
def suggest_task():
    """Get intelligent task suggestion with multi-LLM support"""
    try:
        if use_sqlite:
            tasks = db.get_all_tasks()
        else:
            with open("task_agent/data/tasks.json", "r") as f:
                tasks = json.load(f)
        
        # Try LangChain agent with multi-LLM support
        if langchain_agent.llm:
            result = langchain_agent.suggest_task_with_reasoning(tasks)
            return {
                **result,
                "llm_provider": langchain_agent.llm_type,
                "method": "langchain_multi_llm"
            }
        else:
            # Fallback to RL-only
            chosen = rl.choose_action("state", tasks, epsilon=0.2)
            if not chosen:
                return {"error": "No available tasks"}
            
            q_value = rl.q_table.get(str(chosen['task_id']), 0)
            return {
                "task": chosen,
                "q_value": round(q_value, 3),
                "reasoning": f"RL-only selection (Q-value: {q_value:.3f}). No LLM available.",
                "llm_provider": "none",
                "method": "rl_only"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/feedback/{task_id}/{reward}")
def update_feedback(task_id: int, reward: float):
    """Update task feedback and Q-learning"""
    if not 0 <= reward <= 1:
        raise HTTPException(status_code=400, detail="Reward must be 0-1")
    
    try:
        result = rl.update_q_value(task_id, reward)
        return {
            "task_id": task_id,
            "reward": reward,
            "q_value_change": f"{result['old_q']:.3f} -> {result['new_q']:.3f}",
            "method": "q_learning_update"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete/{task_id}")
def complete_task(task_id: int):
    """Mark task as completed"""
    try:
        if use_sqlite:
            db.update_task_status(task_id, "done")
            return {"task_id": task_id, "status": "done", "method": "sqlite"}
        else:
            with open("task_agent/data/tasks.json", "r") as f:
                tasks = json.load(f)
            
            for task in tasks:
                if task["task_id"] == task_id:
                    task["status"] = "done"
                    break
            else:
                raise HTTPException(status_code=404, detail="Task not found")
            
            with open("task_agent/data/tasks.json", "w") as f:
                json.dump(tasks, f, indent=2)
            
            return {"task_id": task_id, "status": "done", "method": "json"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():
    """Get RL statistics and system status"""
    try:
        stats = rl.get_task_statistics()
        llm_status = detect_llm_capabilities()
        
        return {
            "rl_stats": stats,
            "q_table": rl.q_table,
            "llm_status": llm_status,
            "system": {
                "sqlite_enabled": use_sqlite,
                "total_q_entries": len(rl.q_table)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    import socket
    
    def find_free_port(start_port=8001):
        """Find an available port starting from start_port"""
        for port in range(start_port, start_port + 100):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('127.0.0.1', port))
                    return port
                except OSError:
                    continue
        return None
    
    port = find_free_port(8001)
    if port:
        print(f"Starting server on port {port}")
        uvicorn.run(app, host="127.0.0.1", port=port)
    else:
        print("No available ports found in range 8001-8100")