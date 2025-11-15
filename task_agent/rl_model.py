import json
import numpy as np
from pathlib import Path

class RLModel:
    def __init__(self, memory_path="task_agent/data/agent_memory.json"):
        self.memory_path = memory_path
        self.q_table = self.load_memory()
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        
    def load_memory(self):
        """Load Q-table from JSON file"""
        try:
            with open(self.memory_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            Path(self.memory_path).parent.mkdir(parents=True, exist_ok=True)
            return {}
    
    def save_memory(self):
        """Save Q-table to JSON file"""
        Path(self.memory_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.memory_path, "w") as f:
            json.dump(self.q_table, f, indent=2)
    
    def choose_action(self, state, tasks, epsilon=0.2):
        """Choose action using epsilon-greedy policy"""
        # Filter available tasks (not done)
        available_tasks = [t for t in tasks if t.get('status') != 'done']
        
        if not available_tasks:
            return None
        
        # Epsilon-greedy exploration
        if np.random.rand() < epsilon:
            return np.random.choice(available_tasks)
        
        # Exploitation: choose task with highest Q-value
        best_task = None
        best_q_value = float('-inf')
        
        for task in available_tasks:
            task_id = str(task['task_id'])
            q_value = self.q_table.get(task_id, 0.0)
            
            if q_value > best_q_value:
                best_q_value = q_value
                best_task = task
        
        return best_task or available_tasks[0]
    
    def update_q_value(self, task_id, reward):
        """Update Q-value using Q-learning formula"""
        task_key = str(task_id)
        old_q = self.q_table.get(task_key, 0.0)
        
        # Q-learning update: Q(s,a) = Q(s,a) + α[r + γ*max(Q(s',a')) - Q(s,a)]
        # Simplified version without next state consideration
        new_q = old_q + self.alpha * (reward - old_q)
        
        self.q_table[task_key] = new_q
        self.save_memory()
        
        return {"old_q": old_q, "new_q": new_q}
    
    def get_task_statistics(self):
        """Get statistics about Q-table and learning"""
        if not self.q_table:
            return {
                "total_tasks": 0,
                "avg_q_value": 0.0,
                "max_q_value": 0.0,
                "min_q_value": 0.0,
                "best_task_id": None
            }
        
        q_values = list(self.q_table.values())
        best_task_id = max(self.q_table.keys(), key=lambda k: self.q_table[k])
        
        return {
            "total_tasks": len(self.q_table),
            "avg_q_value": np.mean(q_values),
            "max_q_value": max(q_values),
            "min_q_value": min(q_values),
            "best_task_id": best_task_id
        }