import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from models.habit import Habit

class DatabaseHandler:
    """Handles all database operations for the habit tracker."""
    
    def __init__(self, db_name: str = "habit_tracker.db"):
        """
        Initialize the database handler.
        
        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self) -> None:
        """Create database tables if they don't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create habits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly')),
                    created_date TEXT NOT NULL
                )
            """)
            
            # Create completions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_date TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id)
                )
            """)
            
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection."""
        return sqlite3.connect(self.db_name)

    def save_habits(self, habits: List[Habit]) -> None:
        """
        Save all habits and their completions to the database.
        
        Args:
            habits: List of Habit objects to save
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Clear existing data 
            cursor.execute("DELETE FROM completions")
            cursor.execute("DELETE FROM habits")
            
            for habit in habits:
                # Insert habit
                cursor.execute(
                    "INSERT INTO habits (name, periodicity, created_date) VALUES (?, ?, ?)",
                    (habit.name, habit.periodicity, habit.created_date.isoformat())
                )
                habit_id = cursor.lastrowid
                
                # Insert completions
                for completion in habit.completion_log:
                    cursor.execute(
                        "INSERT INTO completions (habit_id, completed_date) VALUES (?, ?)",
                        (habit_id, completion.isoformat())
                    )
            
            conn.commit()

    def load_habits(self) -> List[Habit]:
        """
        Load all habits and their completions from the database.
        
        Returns:
            List of Habit objects populated with their completion logs
        """
        habits = []
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Get all habits
            cursor.execute("SELECT id, name, periodicity, created_date FROM habits")
            habit_rows = cursor.fetchall()
            
            for habit_row in habit_rows:
                habit_id, name, periodicity, created_date = habit_row
                
                # Get all completions for this habit
                cursor.execute(
                    "SELECT completed_date FROM completions WHERE habit_id = ? ORDER BY completed_date",
                    (habit_id,)
                )
                completion_dates = [row[0] for row in cursor.fetchall()]
                
                # Create Habit object
                habit = Habit(
                    name=name,
                    periodicity=periodicity,
                    created_date=datetime.fromisoformat(created_date)
                )
                
                # Add completions
                for date_str in completion_dates:
                    habit.complete(datetime.fromisoformat(date_str))
                
                habits.append(habit)
        
        return habits

    def add_completion(self, habit_id: int, completion_date: Optional[datetime] = None) -> None:
        """
        Record a habit completion in the database.
        
        Args:
            habit_id: ID of the habit to mark as completed
            completion_date: Optional datetime of completion (defaults to now)
        """
        if completion_date is None:
            completion_date = datetime.now()
            
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO completions (habit_id, completed_date) VALUES (?, ?)",
                (habit_id, completion_date.isoformat())
            )
            conn.commit()

    def delete_habit(self, habit_id: int) -> None:
        """
        Delete a habit and all its completions from the database.
        
        Args:
            habit_id: ID of the habit to delete
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Delete completions first 
            cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
            
            # Delete the habit
            cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            
            conn.commit()

    def clear_all_data(self) -> None:
        """Clear all data from the database (for testing/reset purposes)."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM completions")
            cursor.execute("DELETE FROM habits")
            conn.commit()


# Helper functions for compatibility with main.py
_db_handler = DatabaseHandler()

def load_habits() -> List[Habit]:
    """Load all habits from the database."""
    return _db_handler.load_habits()

def save_habits(habits: List[Habit]) -> None:
    """Save all habits to the database."""
    _db_handler.save_habits(habits)