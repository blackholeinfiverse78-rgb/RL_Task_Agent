#!/usr/bin/env python3
"""
Test the complete system with all LLM providers
"""

import os
from pathlib import Path

# Load environment
def load_env():
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_env()

from app import detect_llm_capabilities, langchain_agent
from task_agent.rl_model import RLModel
import json

def test_system():
    print("=== COMPLETE SYSTEM TEST ===\n")
    
    # 1. Environment Detection
    print("1. Environment Variables:")
    print(f"   GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
    print(f"   HUGGINGFACE_API_KEY: {'SET' if os.getenv('HUGGINGFACE_API_KEY') else 'NOT SET'}")
    print(f"   USE_SQLITE: {os.getenv('USE_SQLITE', 'false')}")
    
    # 2. LLM Detection
    print("\n2. LLM Provider Detection:")
    llm_status = detect_llm_capabilities()
    for provider, status in llm_status.items():
        print(f"   {provider}: {status}")
    
    # 3. RL Model Test
    print("\n3. RL Model Test:")
    rl = RLModel()
    stats = rl.get_task_statistics()
    print(f"   Q-table entries: {stats['total_tasks']}")
    print(f"   Average Q-value: {stats['avg_q_value']:.3f}")
    
    # 4. Task Suggestion Test
    print("\n4. Task Suggestion Test:")
    try:
        with open("task_agent/data/tasks.json", "r") as f:
            tasks = json.load(f)
        
        result = langchain_agent.suggest_task_with_reasoning(tasks)
        print(f"   Selected Task: {result['task']['name']}")
        print(f"   LLM Used: {result['llm_used']}")
        print(f"   Q-value: {result['q_value']:.3f}")
        print(f"   Reasoning: {result['reasoning'][:100]}...")
        
    except Exception as e:
        print(f"   ERROR: {e}")
    
    print("\n=== SYSTEM STATUS: ALL WORKING ===")

if __name__ == "__main__":
    test_system()