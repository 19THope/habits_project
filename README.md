# habits_project
A command-line habit tracking application that helps you build and maintain good habits through streak tracking and analytics.

# Features ✨
  * __Habit Management__: Create daily or weekly habits
  * __Completion Tracking__: Log when you complete your habits
  * __Streak Analytics__: View current and longest streaks
  * __Progress Insights__: Identify broken habits
  * __Data Persistence__: Habits are saved between sessions

# Project Structure 🗂️
 ```
 habits/
  ├── main.py                 # Main application entry point
  ├── analytics/
  │   ├── __init__.py
  │   └── analytics_module.py # All analytical functions
  ├── db/
  │   ├── __init__.py
  │   └── db_handler.py       # Database operations
  ├── models/
  │   ├── __init__.py
  │   └── habit.py           # Habit model definition
  ├── .gitignore
  └── README.md 
```
# Installation ⚙️
1. Clone the repository
    * git clone https://github.com/yourusername/habits.git
    * cd habits
2. Ensure you have Python 3.8+ installed

# Usage 🚀
  Run the application: 
  * python main.py


__Menu Options:__

__1. Create new habit__ - Track a new daily/weekly habit

__2. Mark habit as completed__ - Log a completion

__3. View all habits__ - See all tracked habits

__4. View habits by periodicity__ - Filter daily/weekly habits

__5. View habit analytics__ - See streaks and performance

__6. View streaks__ - Check individual habit streaks

__7. Exit__ - Save and quit

# Example Workflow 📝

1. Create a "Go jogging" daily habit

2. Mark it completed each day you run 

3. View analytics to track your 7-day streak

4. Get notified if you break your streak

# Database Schema 💾
The application uses SQLite with two tables:

### habits

* id (PK)

* name (text)

* periodicity (text: 'daily'/'weekly')

* created_date (text ISO format)

### completions

* id (PK)

* habit_id (FK to habits)

* completed_date (text ISO format)

# Contributing 🤝
Contributions are welcome! Please open an issue or PR for any:

* Bug fixes

* New features

* Documentation improvements

# License 📄