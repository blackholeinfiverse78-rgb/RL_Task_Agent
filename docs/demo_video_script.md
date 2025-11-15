# RL Task Agent Demo Video Script

**Duration:** 2-3 minutes  
**Recording Tool:** OBS Studio / Loom / ScreenPal  
**Resolution:** 1920x1080 recommended

---

## Scene 1: Introduction (0:00 - 0:20)

**Screen:** Desktop with project folder open  
**Narration:**
> "Welcome to the RL Task Agent demo. This is an intelligent task management system that uses Reinforcement Learning combined with AI reasoning to suggest optimal task prioritization. Let me show you how it works."

**Actions:**
- Show project folder structure
- Highlight key files: tasks.json, rl_model.py, demo_app.py

---

## Scene 2: Task Data Overview (0:20 - 0:40)

**Screen:** Open tasks.json in editor  
**Narration:**
> "First, let's look at our task database. We have 10 diverse tasks with comprehensive metadata including priority, complexity, categories, and due dates. Each task represents real-world development work from bug fixes to feature development."

**Actions:**
- Scroll through tasks.json showing different task types
- Highlight key fields: priority, complexity, category, status

---

## Scene 3: Starting the Demo App (0:40 - 1:00)

**Screen:** Terminal and browser  
**Narration:**
> "Now let's launch the Streamlit demo application. This provides an interactive interface to test our RL agent."

**Actions:**
- Run: `streamlit run demo_app.py`
- Show browser opening to localhost:8501
- Quick overview of the interface layout

---

## Scene 4: Task Filtering & Visualization (1:00 - 1:20)

**Screen:** Streamlit app - task list section  
**Narration:**
> "The interface shows all our tasks with filtering capabilities. We can filter by status, priority, or category. Each task displays in an expandable card showing all metadata."

**Actions:**
- Demonstrate filtering by priority (show critical tasks)
- Expand a task card to show full details
- Switch filter to show pending tasks only

---

## Scene 5: AI Task Recommendation (1:20 - 1:50)

**Screen:** Streamlit app - agent controls section  
**Narration:**
> "Here's where the magic happens. The RL agent uses Q-learning with epsilon-greedy exploration to select the best next task. It considers multiple factors: learned Q-values, task priority, complexity, and status."

**Actions:**
- Click "Suggest Next Task" button
- Show the loading spinner
- Display the selected task with details
- Show the AI reasoning explanation from Ollama

---

## Scene 6: Learning Through Feedback (1:50 - 2:10)

**Screen:** Streamlit app - feedback section  
**Narration:**
> "The system learns from feedback. When we provide a reward rating, it updates the Q-table using the Q-learning formula. This helps the agent make better recommendations over time."

**Actions:**
- Adjust the reward slider (set to 0.8)
- Click "Submit Feedback"
- Show the success message
- Highlight that Q-values are updated

---

## Scene 7: Q-Table Visualization (2:10 - 2:30)

**Screen:** Streamlit app - agent memory section  
**Narration:**
> "At the bottom, we can see the agent's memory - the Q-table that stores learned values for each task. We also see learning statistics including total tasks learned, average Q-values, and the best performing task."

**Actions:**
- Scroll to Q-table section
- Show the statistics dashboard
- Point out the JSON Q-table display
- Highlight how values change with learning

---

## Scene 8: API Backend (2:30 - 2:45)

**Screen:** Browser with FastAPI docs  
**Narration:**
> "The system also provides a REST API backend with multiple endpoints for task management, recommendations, and agent statistics. This makes it easy to integrate with existing project management tools."

**Actions:**
- Open http://localhost:8001/docs
- Show the available endpoints
- Demonstrate one API call (GET /tasks)

---

## Scene 9: Conclusion (2:45 - 3:00)

**Screen:** Return to Streamlit app overview  
**Narration:**
> "This RL Task Agent demonstrates how reinforcement learning can be applied to real-world task management. The system continuously learns from feedback, provides explainable recommendations, and scales to handle complex project workflows. Thank you for watching!"

**Actions:**
- Quick scroll through the full interface
- Show the final Q-table state
- End with project folder view

---

## Recording Tips

### Technical Setup
- **Resolution:** 1920x1080 for crisp text
- **Frame Rate:** 30 FPS minimum
- **Audio:** Clear microphone, noise-free environment
- **Browser Zoom:** 125% for better text visibility

### Presentation Tips
- **Pace:** Speak clearly and not too fast
- **Mouse Movement:** Smooth, deliberate movements
- **Highlights:** Use cursor to point to important elements
- **Transitions:** Smooth transitions between screens

### Pre-Recording Checklist
- [ ] Ollama running with llama3 model loaded
- [ ] All dependencies installed
- [ ] Demo app tested and working
- [ ] FastAPI server ready (port 8001)
- [ ] Browser bookmarks set up
- [ ] Screen recording software configured
- [ ] Audio levels tested

### Post-Recording
- [ ] Trim any dead time at start/end
- [ ] Add title slide if needed
- [ ] Export in MP4 format
- [ ] Test playback quality
- [ ] Upload to preferred platform

---

## Alternative 2-Minute Version

If time is limited, focus on:
1. Quick intro (15s)
2. Task recommendation demo (45s)
3. Feedback and learning (30s)
4. Q-table visualization (30s)
5. Conclusion (20s)

This condensed version still shows the core RL learning loop while staying within time constraints.