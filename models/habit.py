from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union


class Habit:
    """
    A class representing a habit to track with name, periodicity, and completion history.
    
    Attributes:
        name (str): The name of the habit.
        periodicity (str): The frequency of the habit ("daily" or "weekly").
        created_date (datetime): When the habit was created.
        completion_log (List[datetime]): Dates when the habit was completed.
    """
    
    VALID_PERIODICITIES = ("daily", "weekly")
    
    def __init__(self, name: str, periodicity: str, created_date: Optional[datetime] = None):
        """
        Initialize a new Habit instance.
        
        Args:
            name: The name of the habit.
            periodicity: The frequency of the habit ("daily" or "weekly").
            created_date: Optional creation date (defaults to now if not provided).
        """
        self.name = name
        self.periodicity = periodicity.lower()
        
        if self.periodicity not in self.VALID_PERIODICITIES:
            raise ValueError(f"Periodicity must be one of: {self.VALID_PERIODICITIES}")
            
        self.created_date = created_date if created_date else datetime.now()
        self.completion_log: List[datetime] = []
    
    def complete(self, completion_time: Optional[Union[datetime, str]] = None) -> None:
        """
        Log a completion of the habit at the given time (or now if not provided).
        
        Args:
            completion_time: Optional time of completion (datetime, ISO string, or None for now).
        """
        if completion_time is None:
            completion_time = datetime.now()
        elif isinstance(completion_time, str):
            try:
                completion_time = datetime.fromisoformat(completion_time)
            except ValueError as e:
                raise ValueError("Invalid ISO format string") from e
                
        self.completion_log.append(completion_time)
        self.completion_log.sort()
    
    def _get_unique_sorted_dates(self) -> List[datetime]:
        """Get sorted unique dates from completion log."""
        if not self.completion_log:
            return []
            
        # Convert to dates and remove duplicates
        unique_dates = list({comp.date() for comp in self.completion_log})
        unique_dates.sort()
        return unique_dates
    
    def get_streaks(self) -> List[int]:
        """
        Calculate all streaks for this habit.
        
        Returns:
            A list of streak lengths in days.
        """
        dates = self._get_unique_sorted_dates()
        if not dates:
            return []
            
        streaks = []
        current_streak = 1
        
        for i in range(1, len(dates)):
            prev_date = dates[i-1]
            current_date = dates[i]
            
            if self.periodicity == "daily":
                expected_next = prev_date + timedelta(days=1)
            else:  # weekly
                expected_next = prev_date + timedelta(weeks=1)
                
            if current_date == expected_next:
                current_streak += 1
            else:
                streaks.append(current_streak)
                current_streak = 1
        
        streaks.append(current_streak)
        return streaks
    
    def get_longest_streak(self) -> int:
        """
        Get the longest streak for this habit.
        
        Returns:
            The length of the longest streak in days.
            Returns 0 if no completions exist.
        """
        streaks = self.get_streaks()
        return max(streaks) if streaks else 0
    
    def get_current_streak(self) -> int:
        """
        Get the current streak (most recent streak).
        
        Returns:
            The length of the current streak in days.
            Returns 0 if no completions exist.
        """
        streaks = self.get_streaks()
        return streaks[-1] if streaks else 0
    
    def is_broken(self, date: Optional[Union[datetime, str]] = None) -> bool:
        """
        Check if the habit is broken as of the given date (or now if not provided).
        
        Args:
            date: Optional date to check (datetime, ISO string, or None for now).
            
        Returns:
            True if the habit is broken, False otherwise.
        """
        if not self.completion_log:
            return True
            
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError as e:
                raise ValueError("Invalid ISO format string") from e
                
        check_date = date.date() if isinstance(date, datetime) else date
        last_completion = max(comp.date() for comp in self.completion_log)
        
        if self.periodicity == "daily":
            expected_next = last_completion + timedelta(days=1)
        else:  # weekly
            expected_next = last_completion + timedelta(weeks=1)
            
        return check_date > expected_next
    
    def __str__(self) -> str:
        """Return a user-friendly string representation of the habit."""
        completions = len(self.completion_log)
        return (
            f"Habit: {self.name} ({self.periodicity}), "
            f"created on {self.created_date.strftime('%Y-%m-%d')}, "
            f"{completions} completion{'s' if completions != 1 else ''}"
        )
    
    def to_dict(self) -> Dict[str, Union[str, List[str]]]:
        """Convert the habit to a dictionary for serialization."""
        return {
            "name": self.name,
            "periodicity": self.periodicity,
            "created_date": self.created_date.isoformat(),
            "completion_log": [comp.isoformat() for comp in sorted(self.completion_log)]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Habit':
        """
        Create a Habit instance from a dictionary.
        
        Args:
            data: Dictionary containing habit data.
            
        Returns:
            A new Habit instance.
        """
        try:
            habit = cls(
                name=data["name"],
                periodicity=data["periodicity"],
                created_date=datetime.fromisoformat(data["created_date"])
            )
            habit.completion_log = [
                datetime.fromisoformat(comp) 
                for comp in data.get("completion_log", [])
            ]
            return habit
        except KeyError as e:
            raise KeyError(f"Missing required key: {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}") from e
