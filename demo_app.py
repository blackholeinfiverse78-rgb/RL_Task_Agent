import streamlit as st
import json
import requests
from pathlib import Path
from task_agent.rl_model import RLModel

def local_llm(prompt: str, model: str = "llama3", timeout: int = 10):
    """Send prompt to local Ollama"""
    try:
        with requests.post("http://localhost:11434/api/generate", 
                          json={"model": model, "prompt": prompt}, 
                          stream=True, timeout=timeout) as r:
            r.raise_for_status()
            text = ""
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            text += data["response"]
                    except:
                        continue
            return text.strip()
    except Exception as e:
        return f"Ollama not available. Using RL-only reasoning. Error: {str(e)}"

st.set_page_config(page_title="RL Task Agent", layout="wide")
st.title("🤖 RL Task Agent Demo")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📋 Tasks")
    
    # Load tasks
    tasks_path = Path("task_agent/data/tasks.json")
    if tasks_path.exists():
        with open(tasks_path, "r") as f:
            tasks = json.load(f)
        st.success(f"Loaded {len(tasks)} tasks")
    else:
        tasks = []
        st.error("No tasks found")
    
    # Task filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        status_filter = st.selectbox("Status", ["All", "pending", "in_progress", "done"])
    with col_f2:
        show_details = st.checkbox("Show Details", value=False)
    
    # Filter tasks
    filtered_tasks = tasks
    if status_filter != "All":
        filtered_tasks = [t for t in tasks if t.get('status') == status_filter]
    
    st.write(f"**{len(filtered_tasks)} tasks**")
    
    # Display tasks
    for task in filtered_tasks:
        status_emoji = {"pending": "⏳", "in_progress": "🔄", "done": "✅"}.get(task.get('status'), "❓")
        
        if show_details:
            with st.expander(f"{status_emoji} Task {task['task_id']}: {task['name']}"):
                st.write(f"**Status:** {task.get('status')}")
                st.write(f"**Reward:** {task.get('reward', 0)}")
        else:
            st.write(f"{status_emoji} **Task {task['task_id']}:** {task['name']}")

with col2:
    st.header("🎯 RL Agent")
    
    epsilon = st.slider("Exploration Rate", 0.0, 1.0, 0.2)
    
    if st.button("🚀 Suggest Next Task", type="primary"):
        with st.spinner("Computing..."):
            rl = RLModel()
            chosen = rl.choose_action("state", tasks, epsilon=epsilon)
            
            if chosen:
                st.session_state.suggested_task = chosen
                st.success("Task Selected!")
                st.write(f"**{chosen['name']}** (ID: {chosen['task_id']})")
                
                # Get AI reasoning
                prompt = f"Explain why '{chosen['name']}' is a good next task in 2 sentences."
                reasoning = local_llm(prompt)
                st.write("**Reasoning:**")
                st.write(reasoning)
            else:
                st.warning("No available tasks")
    
    # Persistent feedback section
    if 'suggested_task' in st.session_state:
        st.write("---")
        st.write(f"**Current Task:** {st.session_state.suggested_task['name']}")
        reward = st.slider("Rate Completion", 0.0, 1.0, 0.5, key="feedback_slider")
        
        col_fb1, col_fb2 = st.columns(2)
        with col_fb1:
            if st.button("Submit Feedback", key="submit_feedback"):
                rl = RLModel()
                rl.update_q_value(st.session_state.suggested_task['task_id'], reward)
                st.success(f"Updated Q-value for Task {st.session_state.suggested_task['task_id']}")
        with col_fb2:
            if st.button("Clear Task", key="clear_task"):
                del st.session_state.suggested_task
                st.rerun()

# Q-table stats
st.write("---")
st.header("📊 Learning Stats")
try:
    rl = RLModel()
    stats = rl.get_task_statistics()
    
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Tasks Learned", stats['total_tasks'])
    with col_s2:
        st.metric("Avg Q-Value", f"{stats['avg_q_value']:.3f}")
    with col_s3:
        st.metric("Best Task", stats.get('best_task_id', 'N/A'))
    
    if st.checkbox("Show Q-Table"):
        st.json(rl.q_table)
        
except Exception as e:
    st.error(f"Error loading stats: {e}")

st.caption("💡 Tip: Use 'Suggest Next Task' to get recommendations, then rate completion to improve future suggestions.")