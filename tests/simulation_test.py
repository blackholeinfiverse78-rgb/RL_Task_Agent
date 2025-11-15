#!/usr/bin/env python3
"""
Simulation script to demonstrate Q-learning updates over 10 iterations
This generates evidence for the learning log documentation.
"""

import json
import random
import sys
sys.path.append('..')
from task_agent.rl_model import RLModel

def run_simulation():
    """Run 10 iterations of task selection and Q-value updates"""
    
    # Initialize RL model
    rl = RLModel()
    
    # Load tasks
    with open("task_agent/data/tasks.json", "r") as f:
        tasks = json.load(f)
    
    print("=== RL Task Agent Simulation - Q-Value Learning Evidence ===\n")
    print("Initial Q-table:", rl.q_table)
    print("\nRunning 10 iterations of task selection and feedback...\n")
    
    for iteration in range(1, 11):
        # Choose action using RL agent
        chosen_task = rl.choose_action("state", tasks, epsilon=0.2)
        
        if chosen_task is None:
            print(f"Iteration {iteration}: No available tasks")
            continue
            
        task_id = chosen_task['task_id']
        task_name = chosen_task['name']
        
        # Simulate realistic reward based on task characteristics
        reward = simulate_reward(chosen_task)
        
        # Update Q-value
        rl.update_q_value(task_id, reward)
        
        # Print iteration results
        print(f"Iteration {iteration}:")
        print(f"  Selected: Task {task_id} - {task_name}")
        print(f"  Priority: {chosen_task.get('priority', 'N/A')}, Complexity: {chosen_task.get('complexity', 'N/A')}")
        print(f"  Reward: {reward:.2f}")
        print(f"  Updated Q-table: {rl.q_table}")
        print()
    
    # Final statistics
    stats = rl.get_task_statistics()
    print("=== Final Statistics ===")
    print(f"Total tasks learned: {stats['total_tasks']}")
    print(f"Average Q-value: {stats['avg_q_value']:.3f}")
    print(f"Best performing task ID: {stats.get('best_task_id', 'N/A')}")
    print(f"Highest Q-value: {stats['max_q_value']:.3f}")
    print(f"Lowest Q-value: {stats['min_q_value']:.3f}")

def simulate_reward(task):
    """Simulate realistic reward based on task characteristics"""
    base_reward = 0.5
    
    # Priority influence
    priority_bonus = {
        'critical': 0.3,
        'high': 0.2,
        'medium': 0.1,
        'low': 0.0
    }.get(task.get('priority', 'medium'), 0.1)
    
    # Complexity influence (easier tasks get slight bonus for completion)
    complexity_bonus = {
        'low': 0.2,
        'medium': 0.1,
        'high': 0.0
    }.get(task.get('complexity', 'medium'), 0.1)
    
    # Add some randomness to simulate real-world variability
    random_factor = random.uniform(-0.1, 0.2)
    
    reward = base_reward + priority_bonus + complexity_bonus + random_factor
    
    # Ensure reward is between 0 and 1
    return max(0.0, min(1.0, reward))

if __name__ == "__main__":
    # Set random seed for reproducible results
    random.seed(42)
    run_simulation()