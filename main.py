import sys
from datetime import datetime
from typing import Optional
from models.habit import Habit
from analytics.analytics_module import (
    get_all_habits,
    filter_habits_by_periodicity,
    get_longest_streak_all_habits,
    get_longest_streak_for_habit,
    get_current_streaks,
    get_broken_habits
)
from db.db_handler import load_habits, save_habits

def display_menu() -> None:
    """Display the main menu options."""
    print("\n👔 Habit Tracker Menu:")
    print("1️⃣  Create new habit")
    print("2️⃣  Mark habit as completed")
    print("3️⃣  View all habits")
    print("4️⃣  View habits by periodicity")
    print("5️⃣ View habit analytics")
    print("6️⃣ View streaks")
    print("7️⃣ Exit")

def create_habit(habits: list[Habit]) -> None:
    """Create a new habit and add it to the list."""
    name = input("Enter habit name: ").strip()
    while not name:
        print("Habit name cannot be empty!")
        name = input("Enter habit name: ").strip()

    periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()
    while periodicity not in ["daily", "weekly"]:
        print("Periodicity must be 'daily' or 'weekly'")
        periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()

    habits.append(Habit(name, periodicity))
    print(f"\nNew habit '{name}' ({periodicity}) created successfully!")

def mark_habit_completed(habits: list[Habit]) -> None:
    """Mark a habit as completed."""
    if not habits:
        print("No habits available. Please create a habit first.")
        return

    print("\nSelect a habit to mark as completed:")
    for i, habit in enumerate(habits, 1):
        print(f"{i}. {habit.name} ({habit.periodicity})")

    try:
        choice = int(input("Enter habit number: ")) - 1
        if 0 <= choice < len(habits):
            habits[choice].complete()
            print(f"\nHabit '{habits[choice].name}' marked as completed!")
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a valid number.")

def view_habits(habits: list[Habit]) -> None:
    """Display all habits."""
    if not habits:
        print("No habits available.")
        return

    print("\nAll Habits:")
    for i, habit in enumerate(habits, 1):
        completions = len(habit.completion_log)
        print(f"{i}. {habit.name} ({habit.periodicity}) - {completions} completion(s)")

def view_habits_by_periodicity(habits: list[Habit]) -> None:
    """Display habits filtered by periodicity."""
    periodicity = input("Enter periodicity to filter by (daily/weekly): ").strip().lower()
    while periodicity not in ["daily", "weekly"]:
        print("Periodicity must be 'daily' or 'weekly'")
        periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()

    filtered = filter_habits_by_periodicity(habits, periodicity)
    if not filtered:
        print(f"No {periodicity} habits available.")
        return

    print(f"\n{periodicity.capitalize()} Habits:")
    for i, habit in enumerate(filtered, 1):
        completions = len(habit.completion_log)
        print(f"{i}. {habit.name} - {completions} completion(s)")

def view_analytics(habits: list[Habit]) -> None:
    """Display habit analytics."""
    if not habits:
        print("No habits available for analytics.")
        return

    print("\nHabit Analytics:")
    
    # Longest streak among all habits
    longest = get_longest_streak_all_habits(habits)
    print(f"\nLongest streak overall: {longest['habit_name']} ({longest['streak_length']} {longest['periodicity']} checks)")
    
    # Current streaks
    print("\nCurrent Streaks:")
    for streak in get_current_streaks(habits):
        print(f"{streak['habit_name']}: {streak['current_streak']} {streak['periodicity']} checks")
    
    # Broken habits
    broken = get_broken_habits(habits)
    if any(h['is_broken'] for h in broken):
        print("\nBroken Habits:")
        for habit in broken:
            if habit['is_broken']:
                last = habit['last_completion'] or "never"
                print(f"{habit['habit_name']} - last completed: {last}")
    else:
        print("\nNo broken habits - good job!")

def view_streaks(habits: list[Habit]) -> None:
    """Display streak information for a specific habit."""
    if not habits:
        print("No habits available.")
        return

    print("\nSelect a habit to view streaks:")
    for i, habit in enumerate(habits, 1):
        print(f"{i}. {habit.name}")

    try:
        choice = int(input("Enter habit number: ")) - 1
        if 0 <= choice < len(habits):
            habit = habits[choice]
            streaks = habit.get_streaks()
            longest = get_longest_streak_for_habit(habit)
            
            print(f"\nStreak analysis for '{habit.name}':")
            print(f"Longest streak: {longest['streak_length']} {habit.periodicity} checks")
            print(f"Current streak: {habit.get_current_streak()} {habit.periodicity} checks")
            
            if streaks:
                print("\nAll streaks:")
                for i, streak in enumerate(streaks, 1):
                    print(f"{i}. {streak} {habit.periodicity} checks")
        else:
            print("Invalid habit number.")
    except ValueError:
        print("Please enter a valid number.")

def main() -> None:
    """Main application loop."""
    print("Welcome to the Habit Tracker!")
    
    # Load existing habits
    habits = load_habits()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()
        
        try:
            if choice == "1":
                create_habit(habits)
            elif choice == "2":
                mark_habit_completed(habits)
            elif choice == "3":
                view_habits(habits)
            elif choice == "4":
                view_habits_by_periodicity(habits)
            elif choice == "5":
                view_analytics(habits)
            elif choice == "6":
                view_streaks(habits)
            elif choice == "7":
                save_habits(habits)
                print("\nYour habits have been saved. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1-7.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()