import os
import json
import requests
from pathlib import Path
from task_agent.rl_model import RLModel

# Load environment variables
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

class LangChainTaskAgent:
    def __init__(self):
        self.rl = RLModel()
        self.llm = self._init_llm()
        self.llm_type = self._get_llm_type()
        
    def _init_llm(self):
        """Initialize LLM with priority: Gemini > HuggingFace > Ollama"""
        # 1. Try Gemini (primary)
        gemini_key = os.getenv("GEMINI_API_KEY")
        if gemini_key and gemini_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=gemini_key)
                return genai.GenerativeModel("gemini-pro")
            except ImportError:
                print("Gemini library not installed")
            except Exception as e:
                print(f"Gemini initialization failed: {e}")
        
        # 2. Try HuggingFace (fallback)
        hf_key = os.getenv("HUGGINGFACE_API_KEY")
        if hf_key and hf_key != "your_huggingface_api_key_here":
            try:
                from langchain_community.llms import HuggingFacePipeline
                return HuggingFacePipeline.from_model_id(
                    model_id="microsoft/DialoGPT-medium",
                    task="text-generation"
                )
            except ImportError:
                print("HuggingFace library not installed")
            except Exception as e:
                print(f"HuggingFace initialization failed: {e}")
        
        # 3. Try Ollama (local fallback)
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                return "ollama"  # Ollama is available
        except:
            pass
        
        return None
    
    def _get_llm_type(self):
        """Get the type of LLM being used"""
        if self.llm is None:
            return "none"
        elif isinstance(self.llm, str) and self.llm == "ollama":
            return "ollama"
        elif 'genai' in str(type(self.llm)) or 'GenerativeModel' in str(type(self.llm)):
            return "gemini"
        elif 'HuggingFace' in str(type(self.llm)):
            return "huggingface"
        else:
            return "unknown"
    
    def suggest_task_with_reasoning(self, tasks):
        """Use RL + LangChain for task recommendation"""
        if not tasks:
            return {"error": "No tasks found"}
        
        # RL selects task
        chosen = self.rl.choose_action("state", tasks)
        if not chosen:
            return {"error": "No available tasks"}
        
        # Get reasoning based on available LLM
        reasoning = self._get_reasoning(chosen)
        
        return {
            "task": chosen,
            "reasoning": reasoning,
            "q_value": self.rl.q_table.get(str(chosen['task_id']), 0),
            "llm_used": self.llm_type
        }
    
    def _get_reasoning(self, task):
        """Generate reasoning using available LLM"""
        prompt = f"Explain why task '{task['name']}' (ID: {task['task_id']}) is the best next choice in 2 sentences."
        
        # Try Gemini first
        if self.llm_type == "gemini":
            try:
                response = self.llm.generate_content(prompt)
                return response.text if hasattr(response, 'text') else str(response)
            except Exception as e:
                # Fallback to HuggingFace if Gemini fails
                if os.getenv("HUGGINGFACE_API_KEY"):
                    try:
                        from langchain_community.llms import HuggingFacePipeline
                        hf_llm = HuggingFacePipeline.from_model_id(
                            model_id="microsoft/DialoGPT-medium",
                            task="text-generation"
                        )
                        return hf_llm(prompt)
                    except:
                        pass
                return f"Gemini failed, HF unavailable: {str(e)[:50]}..."
        
        # Try HuggingFace
        elif self.llm_type == "huggingface":
            try:
                return self.llm(prompt)
            except Exception as e:
                return f"HuggingFace failed: {str(e)}"
        
        # Try Ollama
        elif self.llm_type == "ollama":
            try:
                response = requests.post("http://localhost:11434/api/generate", 
                                       json={"model": "llama3", "prompt": prompt}, 
                                       timeout=10)
                if response.status_code == 200:
                    text = ""
                    for line in response.iter_lines(decode_unicode=True):
                        if line:
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    text += data["response"]
                            except:
                                continue
                    return text.strip() or "Ollama response empty"
                else:
                    return "Ollama server error"
            except Exception as e:
                return f"Ollama failed: {str(e)}"
        
        # Fallback to RL-only reasoning
        q_val = self.rl.q_table.get(str(task['task_id']), 0)
        priority = task.get('priority', 'medium')
        status = task.get('status', 'unknown')
        return f"Task '{task['name']}' selected by RL agent (Q-value: {q_val:.3f}). Priority: {priority}, Status: {status}. This task shows good learning potential based on historical performance."