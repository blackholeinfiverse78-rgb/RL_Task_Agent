import sqlite3
import json
from pathlib import Path

class TaskDatabase:
    def __init__(self, db_path="task_agent/data/tasks.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def init_db(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    reward REAL DEFAULT 0.0
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS q_values (
                    task_id TEXT PRIMARY KEY,
                    q_value REAL DEFAULT 0.0
                )
            """)
    
    def get_all_tasks(self):
        """Get all tasks"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tasks_by_status(self, status):
        """Get tasks by status"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM tasks WHERE status = ?", (status,))
            return [dict(row) for row in cursor.fetchall()]
    
    def add_task(self, task_id, name, status="pending"):
        """Add new task"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO tasks (task_id, name, status) VALUES (?, ?, ?)", 
                        (task_id, name, status))
    
    def update_task_status(self, task_id, status, reward=None):
        """Update task status and reward"""
        with sqlite3.connect(self.db_path) as conn:
            if reward is not None:
                conn.execute("UPDATE tasks SET status = ?, reward = ? WHERE task_id = ?", 
                           (status, reward, task_id))
            else:
                conn.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (status, task_id))
    
    def get_q_table(self):
        """Get Q-table as dictionary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT task_id, q_value FROM q_values")
            return {row[0]: row[1] for row in cursor.fetchall()}
    
    def update_q_value(self, task_id, q_value):
        """Update Q-value"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO q_values (task_id, q_value) VALUES (?, ?)", 
                        (str(task_id), q_value))
    
    def migrate_from_json(self):
        """Migrate from JSON to SQLite"""
        try:
            # Migrate tasks
            with open("task_agent/data/tasks.json", 'r') as f:
                tasks = json.load(f)
            
            for task in tasks:
                self.add_task(task['task_id'], task['name'], task.get('status', 'pending'))
                if task.get('reward', 0) > 0:
                    self.update_task_status(task['task_id'], task['status'], task['reward'])
            
            # Migrate Q-table
            with open("task_agent/data/agent_memory.json", 'r') as f:
                q_table = json.load(f)
            
            for task_id, q_value in q_table.items():
                self.update_q_value(task_id, q_value)
                
        except FileNotFoundError:
            pass