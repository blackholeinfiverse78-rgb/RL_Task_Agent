#!/usr/bin/env python3
"""
Simple 6-step RL workflow demo
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from task_agent.rl_model import RLModel

def run_workflow():
    """Execute the 6-step RL workflow"""
    
    # Step 1: Input - Load tasks
    print("Step 1: Input - Loading tasks...")
    with open("task_agent/data/tasks.json", "r") as f:
        tasks = json.load(f)
    print(f"Loaded {len(tasks)} tasks")
    
    # Step 2: State - Analyze current state
    print("\nStep 2: State - Analyzing current state...")
    pending = [t for t in tasks if t['status'] == 'pending']
    completed = [t for t in tasks if t['status'] == 'done']
    in_progress = [t for t in tasks if t['status'] == 'in_progress']
    
    print(f"  Pending: {len(pending)}")
    print(f"  Completed: {len(completed)}")
    print(f"  In Progress: {len(in_progress)}")
    
    # Step 3: Action - Agent chooses next task
    print("\nStep 3: Action - Agent choosing next best task...")
    rl = RLModel()
    chosen_task = rl.choose_action("state", pending, epsilon=0.1)
    
    if chosen_task:
        print(f"  Selected: Task {chosen_task['task_id']} - {chosen_task['name']}")
    else:
        print("  No tasks available")
        return
    
    # Step 4: Reward - Simulate task completion
    print("\nStep 4: Reward - Task completion feedback...")
    reward = float(input(f"Rate task completion (0.0-1.0): ") or "0.8")
    print(f"  Reward: {reward}")
    
    # Step 5: Update - Agent updates Q-table
    print("\nStep 5: Update - Updating Q-table...")
    old_q = rl.q_table.get(str(chosen_task['task_id']), 0)
    rl.update_q_value(chosen_task['task_id'], reward)
    new_q = rl.q_table.get(str(chosen_task['task_id']), 0)
    print(f"  Q-value: {old_q:.3f} -> {new_q:.3f}")
    
    # Step 6: Output - Suggest new order
    print("\nStep 6: Output - New task recommendations...")
    remaining_tasks = [t for t in pending if t['task_id'] != chosen_task['task_id']]
    
    # Sort by Q-values and priority
    task_scores = []
    for task in remaining_tasks:
        q_val = rl.q_table.get(str(task['task_id']), 0)
        task_scores.append((task, q_val))
    
    task_scores.sort(key=lambda x: x[1], reverse=True)
    
    print("  Recommended order:")
    for i, (task, score) in enumerate(task_scores[:5], 1):
        print(f"    {i}. Task {task['task_id']}: {task['name']} (Q: {score:.3f})")

if __name__ == "__main__":
    run_workflow()