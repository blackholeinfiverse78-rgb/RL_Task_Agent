import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Define colors
blue = '#4A90E2'
green = '#7ED321'
orange = '#F5A623'
red = '#D0021B'
purple = '#9013FE'

# Title
ax.text(5, 7.5, 'RL Task Agent Flow Diagram', fontsize=20, fontweight='bold', ha='center')

# State box
state_box = FancyBboxPatch((0.5, 5.5), 2, 1, boxstyle="round,pad=0.1", 
                          facecolor=blue, edgecolor='black', linewidth=2)
ax.add_patch(state_box)
ax.text(1.5, 6, 'STATE\nTask List\n+ Q-table', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# Action box
action_box = FancyBboxPatch((4, 5.5), 2, 1, boxstyle="round,pad=0.1", 
                           facecolor=green, edgecolor='black', linewidth=2)
ax.add_patch(action_box)
ax.text(5, 6, 'ACTION\nSelect Task\n(ε-greedy)', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# LLM Reasoning box
llm_box = FancyBboxPatch((7.5, 5.5), 2, 1, boxstyle="round,pad=0.1", 
                        facecolor=purple, edgecolor='black', linewidth=2)
ax.add_patch(llm_box)
ax.text(8.5, 6, 'LLM\nReasoning\n(Ollama)', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# Reward box
reward_box = FancyBboxPatch((7.5, 3), 2, 1, boxstyle="round,pad=0.1", 
                           facecolor=orange, edgecolor='black', linewidth=2)
ax.add_patch(reward_box)
ax.text(8.5, 3.5, 'REWARD\nUser Feedback\n(0.0 - 1.0)', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# Update box
update_box = FancyBboxPatch((4, 3), 2, 1, boxstyle="round,pad=0.1", 
                           facecolor=red, edgecolor='black', linewidth=2)
ax.add_patch(update_box)
ax.text(5, 3.5, 'UPDATE\nQ-learning\nFormula', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# Memory box
memory_box = FancyBboxPatch((0.5, 3), 2, 1, boxstyle="round,pad=0.1", 
                           facecolor='gray', edgecolor='black', linewidth=2)
ax.add_patch(memory_box)
ax.text(1.5, 3.5, 'MEMORY\nPersistent\nQ-table', fontsize=10, ha='center', va='center', color='white', fontweight='bold')

# Arrows
# State to Action
ax.arrow(2.5, 6, 1.3, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(3.25, 6.3, 'Multi-factor\nScoring', fontsize=8, ha='center')

# Action to LLM
ax.arrow(6, 6, 1.3, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(6.75, 6.3, 'Explain\nChoice', fontsize=8, ha='center')

# LLM to Reward (curved)
ax.annotate('', xy=(8.5, 4), xytext=(8.5, 5.5), 
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.text(9, 4.75, 'Execute\n& Rate', fontsize=8, ha='center')

# Reward to Update
ax.arrow(7.5, 3.5, -1.3, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(6.75, 3.8, 'Feedback\nSignal', fontsize=8, ha='center')

# Update to Memory
ax.arrow(4, 3.5, -1.3, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.text(3.25, 3.8, 'Store\nLearning', fontsize=8, ha='center')

# Memory to State (curved)
ax.annotate('', xy=(1.5, 5.5), xytext=(1.5, 4), 
            arrowprops=dict(arrowstyle='->', lw=2, color='black'))
ax.text(0.8, 4.75, 'Load\nHistory', fontsize=8, ha='center')

# Q-learning formula
ax.text(5, 1.5, 'Q-Learning Update Formula:', fontsize=12, ha='center', fontweight='bold')
ax.text(5, 1, r'$Q(s,a) \leftarrow Q(s,a) + \alpha [r + \gamma \max Q(s\',a\') - Q(s,a)]$', 
        fontsize=14, ha='center', style='italic')
ax.text(5, 0.5, 'α = learning rate (0.1), γ = discount factor (0.9)', fontsize=10, ha='center')

plt.tight_layout()
plt.savefig('rl_flow_diagram.png', dpi=300, bbox_inches='tight')
plt.show()
print("RL Flow Diagram saved as 'rl_flow_diagram.png'")