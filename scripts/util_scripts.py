#!/usr/bin/env python3
"""
Utility scripts for RL Task Agent
"""

import json
import os
from pathlib import Path

def reset_project():
    """Reset tasks and Q-table to empty state"""
    tasks_path = Path("task_agent/data/tasks.json")
    memory_path = Path("task_agent/data/agent_memory.json")
    
    # Clear tasks
    with open(tasks_path, "w") as f:
        json.dump([], f)
    
    # Clear Q-table
    with open(memory_path, "w") as f:
        json.dump({}, f)
    
    print("Project reset: tasks and Q-table cleared")

def add_sample_tasks():
    """Add sample tasks for testing"""
    sample_tasks = [
        {"task_id": 1, "name": "Fix bug", "status": "pending", "reward": 0},
        {"task_id": 2, "name": "Write docs", "status": "pending", "reward": 0},
        {"task_id": 3, "name": "Add tests", "status": "pending", "reward": 0},
        {"task_id": 4, "name": "Deploy app", "status": "done", "reward": 1},
        {"task_id": 5, "name": "Code review", "status": "pending", "reward": 0}
    ]
    
    with open("task_agent/data/tasks.json", "w") as f:
        json.dump(sample_tasks, f, indent=2)
    
    print(f"Added {len(sample_tasks)} sample tasks")

def show_project_status():
    """Show current project status"""
    try:
        with open("task_agent/data/tasks.json", "r") as f:
            tasks = json.load(f)
        
        with open("task_agent/data/agent_memory.json", "r") as f:
            q_table = json.load(f)
        
        pending = len([t for t in tasks if t.get('status') == 'pending'])
        done = len([t for t in tasks if t.get('status') == 'done'])
        
        print(f"Tasks: {len(tasks)} total, {pending} pending, {done} done")
        print(f"Q-table: {len(q_table)} entries")
        
    except FileNotFoundError:
        print("No data files found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python util_scripts.py [reset|sample|status]")
    elif sys.argv[1] == "reset":
        reset_project()
    elif sys.argv[1] == "sample":
        add_sample_tasks()
    elif sys.argv[1] == "status":
        show_project_status()
    else:
        print("Unknown command")