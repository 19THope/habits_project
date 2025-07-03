from datetime import datetime
from typing import List, Dict, Optional, Union # Typing allows us to annotate return types and function signatures
from models.habit import Habit  


def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """
    Return a list of all currently tracked habits.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of all habits
    """
    return habits.copy()


def filter_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    Return a list of all habits with the specified periodicity.
    
    Args:
        habits: List of Habit objects
        periodicity: Either 'daily' or 'weekly'
        
    Returns:
        Filtered list of habits
    """
    if periodicity.lower() not in ('daily', 'weekly'):
        raise ValueError("Periodicity must be either 'daily' or 'weekly'")
    
    return [habit for habit in habits if habit.periodicity == periodicity.lower()]


def get_longest_streak_all_habits(habits: List[Habit]) -> Dict[str, Union[str, int]]:
    """
    Return the longest run streak among all defined habits.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        Dictionary with:
        - 'habit_name': name of the habit with longest streak
        - 'streak_length': length of the longest streak
        - 'periodicity': periodicity of the habit
    """
    if not habits:
        raise ValueError("No habits provided")
    
    streaks = [
        {
            'habit_name': habit.name,
            'streak_length': habit.get_longest_streak(),
            'periodicity': habit.periodicity
        }
        for habit in habits
    ]
    
    return max(streaks, key=lambda x: x['streak_length'])


def get_longest_streak_for_habit(habit: Habit) -> Dict[str, Union[str, int]]:
    """
    Return the longest run streak for a given habit.
    
    Args:
        habit: A Habit object
        
    Returns:
        Dictionary with:
        - 'habit_name': name of the habit
        - 'streak_length': length of the longest streak
        - 'periodicity': periodicity of the habit
    """
    return {
        'habit_name': habit.name,
        'streak_length': habit.get_longest_streak(),
        'periodicity': habit.periodicity
    }


def get_habits_sorted_by_streak(habits: List[Habit], descending: bool = True) -> List[Dict[str, Union[str, int]]]:
    """
    Get all habits sorted by their longest streak length.
    
    Args:
        habits: List of Habit objects
        descending: Whether to sort in descending order (default True)
        
    Returns:
        List of dictionaries with habit streak information, sorted
    """
    streaks = [get_longest_streak_for_habit(habit) for habit in habits]
    return sorted(
        streaks,
        key=lambda x: x['streak_length'],
        reverse=descending
    )


def get_current_streaks(habits: List[Habit]) -> List[Dict[str, Union[str, int]]]:
    """
    Get current streaks for all habits.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of dictionaries with current streak information
    """
    return [
        {
            'habit_name': habit.name,
            'current_streak': habit.get_current_streak(),
            'periodicity': habit.periodicity
        }
        for habit in habits
    ]


def get_broken_habits(habits: List[Habit], as_of_date: Optional[datetime] = None) -> List[Dict[str, Union[str, bool, Optional[str]]]]:
    """
    Get list of habits that are currently broken.
    
    Args:
        habits: List of Habit objects
        as_of_date: Optional date to check (defaults to now)
        
    Returns:
        List of dictionaries with broken status information
    """
    return [
        {
            'habit_name': habit.name,
            'is_broken': habit.is_broken(as_of_date),
            'periodicity': habit.periodicity,
            'last_completion': max(habit.completion_log).isoformat() if habit.completion_log else None
        }
        for habit in habits
    ]