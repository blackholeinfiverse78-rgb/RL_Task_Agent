#!/usr/bin/env python3
"""
Load environment variables from .env file
"""

import os
from pathlib import Path

def load_env():
    """Load .env file manually"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("Environment variables loaded from .env")
    else:
        print("No .env file found")

if __name__ == "__main__":
    load_env()
    print("Current environment:")
    print(f"GEMINI_API_KEY: {'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET'}")
    print(f"HUGGINGFACE_API_KEY: {'SET' if os.getenv('HUGGINGFACE_API_KEY') else 'NOT SET'}")
    print(f"USE_SQLITE: {os.getenv('USE_SQLITE', 'false')}")