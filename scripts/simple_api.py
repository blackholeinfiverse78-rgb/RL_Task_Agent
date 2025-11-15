#!/usr/bin/env python3
"""
Simple API that follows the 6-step workflow
"""

from fastapi import FastAPI
import json
from task_agent.rl_model import RLModel

app = FastAPI(title="Simple RL Task Workflow")
rl = RLModel()

@app.get("/")
def workflow_status():
    """Get current workflow state"""
    with open("task_agent/data/tasks.json", "r") as f:
        tasks = json.load(f)
    
    pending = len([t for t in tasks if t['status'] == 'pending'])
    completed = len([t for t in tasks if t['status'] == 'done'])
    
    return {
        "step": "Ready for workflow",
        "total_tasks": len(tasks),
        "pending": pending,
        "completed": completed
    }

@app.post("/workflow/step3")
def choose_next_task():
    """Step 3: Agent chooses next best task"""
    with open("task_agent/data/tasks.json", "r") as f:
        tasks = json.load(f)
    
    pending = [t for t in tasks if t['status'] == 'pending']
    chosen = rl.choose_action("state", pending, epsilon=0.1)
    
    if not chosen:
        return {"error": "No pending tasks"}
    
    return {
        "step": 3,
        "action": "Task selected",
        "chosen_task": {
            "id": chosen['task_id'],
            "name": chosen['name']
        }
    }

@app.post("/workflow/step5/{task_id}/{reward}")
def update_learning(task_id: int, reward: float):
    """Step 5: Update Q-table with reward"""
    old_q = rl.q_table.get(str(task_id), 0)
    rl.update_q_value(task_id, reward)
    new_q = rl.q_table.get(str(task_id), 0)
    
    return {
        "step": 5,
        "update": "Q-table updated",
        "task_id": task_id,
        "reward": reward,
        "q_value_change": f"{old_q:.3f} -> {new_q:.3f}"
    }

@app.get("/workflow/step6")
def get_recommendations():
    """Step 6: Get new task order recommendations"""
    with open("task_agent/data/tasks.json", "r") as f:
        tasks = json.load(f)
    
    pending = [t for t in tasks if t['status'] == 'pending']
    
    # Sort by Q-values
    recommendations = []
    for task in pending:
        q_val = rl.q_table.get(str(task['task_id']), 0)
        recommendations.append({
            "task_id": task['task_id'],
            "name": task['name'],
            "q_value": round(q_val, 3)
        })
    
    recommendations.sort(key=lambda x: x['q_value'], reverse=True)
    
    return {
        "step": 6,
        "output": "Task recommendations",
        "recommended_order": recommendations[:10]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)