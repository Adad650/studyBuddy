import datetime

# ==========================================
# MODULE 0: APP OVERVIEW & DATA STRUCTURE
# ==========================================

# Data models (stored in memory; saved to disk as JSON/CSV)
# Task:
#   id (int)
#   title (string)
#   details (string)
#   due_date (date or None)
#   priority (int: 1=high, 2=med, 3=low)
#   tags (list of strings)
#   status (enum: "todo", "doing", "done")
#   created_at (datetime)
#   completed_at (datetime or None)
# template for a task


# template for a task
data = {
    "title": "",
    "details": "",
    "dueDate": "",
    "priority": None,
    "tags": [],
    "status": "todo",
    "createdAt": "",
    "completedAt": None,
    "flashCards": []
}

tasks = []
userWant = True


def createTask():
    try:
        task = data.copy()

        task["title"] = input("Input task name:  ")
        task["details"] = input("Input task Description: ")
        task["dueDate"] = input("Input task due date: ")
        task["priority"] = int(input("Priority (1=high, 2=medium, 3=low): "))
        task["tags"] = input("Input task tags (comma separated): ").split(",")
        task["status"] = input("Input task status (todo/doing/done): ")
        task["createdAt"] = str(datetime.datetime.now())

        flashCardQuantity = int(input("How many flash cards do you want to make? "))
        for i in range(flashCardQuantity):
            print(f"\n--- Flashcard {i+1} ---")
            card_title = input("Flashcard Title: ")
            card_text = input("Flashcard Text: ")
            flashCard = {"Title": card_title, "Text": card_text}
            task["flashCards"].append(flashCard)

        return task
    except Exception as e:
        print("⚠️ Error creating task:", e)
        return None


def editTask(task):
    try:
        while True:
            print("\n\nEditing Task:", task["title"])
            choice = int(input(
                "Choose what to edit:\n"
                "1. Title\n2. Details\n3. Due Date\n4. Priority\n5. Tags\n"
                "6. Status\n7. Flashcards\n8. Back\n"
            ))

            if choice == 1:
                task["title"] = input("New title: ")
            elif choice == 2:
                task["details"] = input("New details: ")
            elif choice == 3:
                task["dueDate"] = input("New due date: ")
            elif choice == 4:
                task["priority"] = int(input("New priority (1=high, 2=medium, 3=low): "))
            elif choice == 5:
                task["tags"] = input("New tags (comma separated): ").split(",")
            elif choice == 6:
                task["status"] = input("New status (todo/doing/done): ")
                if task["status"] == "done":
                    task["completedAt"] = str(datetime.datetime.now())
            elif choice == 7:
                sub = int(input("1. Add flashcard\n2. Edit flashcard\n3. Delete flashcard\n4. Back\n"))
                if sub == 1:
                    card_title = input("Flashcard Title: ")
                    card_text = input("Flashcard Text: ")
                    task["flashCards"].append({"Title": card_title, "Text": card_text})
                elif sub == 2 and task["flashCards"]:
                    for i, card in enumerate(task["flashCards"], start=1):
                        print(f"{i}. {card['Title']} - {card['Text']}")
                    idx = int(input("Select card number to edit: ")) - 1
                    if 0 <= idx < len(task["flashCards"]):
                        task["flashCards"][idx]["Title"] = input("New title: ")
                        task["flashCards"][idx]["Text"] = input("New text: ")
                elif sub == 3 and task["flashCards"]:
                    for i, card in enumerate(task["flashCards"], start=1):
                        print(f"{i}. {card['Title']} - {card['Text']}")
                    idx = int(input("Select card number to delete: ")) - 1
                    if 0 <= idx < len(task["flashCards"]):
                        task["flashCards"].pop(idx)
            elif choice == 8:
                break
            else:
                print("Invalid choice.")
    except Exception as e:
        print("Error editing task:", e)


# main loop wrapped in try/except
while userWant:
    try:
        choice = int(input("Choose an option:\n1. Add a new task\n2. View all tasks\n3. View individual task\n4. Edit\n5. Exit\n"))
        match choice:
            case 1:
                new_task = createTask()
                if new_task:  # only append if task was successfully created
                    tasks.append(new_task)
                    print("\nNew task created and added to list!")
            case 2:
                print("\nCurrent Tasks:")
                for i, t in enumerate(tasks, start=1):
                    print(f"{i}. {t['title']} - {t['status']}")
            case 3:
                taskToView = input("Input Task name:  ")
                found = False
                for t in tasks:
                    if t["title"].lower() == taskToView.lower():
                        print("\n🔎 Task Details:")
                        for key, value in t.items():
                            print(f"{key}: {value}")
                        found = True
                        break
                if not found:
                    print("Task not found.")
            case 4:
                if not tasks:
                    print("No tasks to edit.")
                else:
                    for i, t in enumerate(tasks, start=1):
                        print(f"{i}. {t['title']} - {t['status']}")
                    edit_index = int(input("Select task number to edit: ")) - 1
                    if 0 <= edit_index < len(tasks):
                        editTask(tasks[edit_index])
                    else:
                        print("Invalid selection.")
            case 5:
                print("Goodbye!")
                userWant = False
            case _:
                print("Invalid choice.")
    except Exception as e:
        print("⚠️ An error occurred in main loop:", e)







# Flashcard:
#   id (int)
#   front (string)
#   back (string)
#   deck (string)
#   ease (float)           # SM-2 like metric
#   interval_days (int)    # next wait time
#   repetitions (int)      # successful review streak
#   next_review (date)

# PomodoroSessionLog:
#   id (int)
#   task_id (int or None)
#   start_time (datetime)
#   end_time (datetime)
#   duration_minutes (int)
#   label (string)         # e.g. "Math", "English", "Coding"
#   successful (bool)

# Persistent files:
#   tasks.json
#   cards.json
#   pomodoros.json
#   (optional exports: tasks.csv, stats.csv)


# ==========================================
# MODULE 1: MAIN MENU + ROUTER
# ==========================================

# On start:
#   # load data from disk (if files exist), otherwise start with empty lists

# Show Main Menu (loop until exit):
#   1) Tasks
#   2) Flashcards
#   3) Pomodoro Timer
#   4) Stats & Reports
#   5) Import/Export
#   6) Settings
#   7) Save & Exit

# Get user choice
# Route to corresponding module function
# Handle invalid input with a friendly message


# ==========================================
# MODULE 2: TASKS
# ==========================================

# Tasks Menu:
#   1) Add Task
#   2) List Tasks (with filters/sorts)
#   3) Update Task (edit fields, change status)
#   4) Complete Task
#   5) Delete Task
#   6) Back

# Add Task:
#   # prompt for title, details, optional due_date, priority, tags
#   # generate id
#   # set status="todo", created_at=now, completed_at=None
#   # append to tasks list

# List Tasks:
#   # ask for optional filter: by status, priority, tag, due_before, search text
#   # ask for optional sort: by due_date, priority, created_at
#   # display numbered table of tasks with key info

# Update Task:
#   # select task by number/id
#   # choose field(s) to change: title/details/due_date/priority/tags/status
#   # apply changes

# Complete Task:
#   # select task
#   # set status="done", completed_at=now

# Delete Task:
#   # select task, confirm deletion, remove from list


# ==========================================
# MODULE 3: FLASHCARDS (SPACED REPETITION)
# ==========================================

# Flashcards Menu:
#   1) Add Card
#   2) Review Due Cards
#   3) Browse Decks / Search
#   4) Edit/Delete Card
#   5) Back

# Add Card:
#   # prompt for front, back, deck name
#   # id=next id
#   # initialize ease=2.5, interval_days=1, repetitions=0
#   # next_review=today
#   # add to list

# Review Due Cards:
#   # select deck or "all"
#   # filter cards where next_review <= today
#   # if none due, print "No cards due"
#   # else loop over due cards:
#       # show front
#       # wait for user to press enter to reveal back
#       # ask user rating: "again", "hard", "good", "easy"
#       # update scheduling using simplified SM-2 rules:
#          # if "again": repetitions=0; interval_days=1; ease=max(1.3, ease-0.2)
#          # if "hard":  repetitions+=1; interval_days=max(1, round(interval_days*1.2)); ease=max(1.3, ease-0.05)
#          # if "good":  repetitions+=1; interval_days=round(interval_days*ease)
#          # if "easy":  repetitions+=1; ease+=0.1; interval_days=round(interval_days*ease*1.2)
#       # set next_review = today + interval_days

# Browse/Search:
#   # choose deck or search text
#   # list matching cards (id, deck, truncated front/back)

# Edit/Delete:
#   # select card by id
#   # choose to edit fields or delete


# ==========================================
# MODULE 4: POMODORO TIMER
# ==========================================

# Pomodoro Menu:
#   1) Start Focus Session (e.g., 25 min)
#   2) Start Short Break (e.g., 5 min)
#   3) Start Long Break (e.g., 15 min)
#   4) Customize Durations
#   5) Back

# Start Focus Session:
#   # optionally select a task_id or enter a label
#   # record start_time=now
#   # countdown for focus_minutes (display remaining time every second or 10s)
#   # on finish: play beep/text notice
#   # ask: "Mark as successful? (y/n)"
#   # log PomodoroSessionLog with end_time=now, duration_minutes, successful flag

# Break Sessions:
#   # similar countdown; no logging unless you want to track breaks

# Customize Durations:
#   # allow user to set focus/short/long durations in minutes
#   # store in settings


# ==========================================
# MODULE 5: STATS & REPORTS
# ==========================================

# Stats Menu:
#   1) Today Overview
#   2) Weekly Summary
#   3) Task Progress
#   4) Flashcard Health
#   5) Export Stats Snapshot
#   6) Back

# Today Overview:
#   # show number of pomodoros done today, total focus minutes
#   # list tasks completed today
#   # number of flashcards reviewed today

# Weekly Summary:
#   # compute last 7 days of pomodoros per day
#   # show heatmap-like text or simple bar lengths using characters
#   # list top 3 tags/labels by focus time

# Task Progress:
#   # count tasks by status
#   # show tasks nearing due date (e.g., due within 2 days)

# Flashcard Health:
#   # total cards, due today, average ease, average interval
#   # decks ranked by due load

# Export Stats Snapshot:
#   # write a CSV or JSON "stats.csv" with daily totals, tasks completed, cards reviewed


# ==========================================
# MODULE 6: IMPORT/EXPORT
# ==========================================

# Import/Export Menu:
#   1) Export Tasks to CSV
#   2) Export Pomodoros to CSV
#   3) Export Flashcards to CSV
#   4) Import Tasks from CSV
#   5) Import Flashcards from CSV
#   6) Back

# Export:
#   # convert lists to CSV rows with headers
#   # write files to disk

# Import:
#   # read CSV, validate columns
#   # map fields, append to in-memory lists
#   # avoid id collisions by remapping ids if needed


# ==========================================
# MODULE 7: SETTINGS
# ==========================================

# Settings structure:
#   theme (light/dark or plain text flair)
#   date_format (e.g., YYYY-MM-DD)
#   pomodoro_durations (focus, short_break, long_break)
#   autosave_interval_minutes (e.g., 5)
#   default_deck

# Settings Menu:
#   # view current settings
#   # edit any field
#   # confirm save

# Autosave Daemon (optional):
#   # background loop that triggers save every N minutes if changes exist


# ==========================================
# MODULE 8: SAVE/LOAD & APP LIFECYCLE
# ==========================================

# Save function:
#   # serialize tasks/cards/pomodoros/settings to JSON files

# Load function:
#   # if files exist, parse JSON into data structures
#   # if parsing fails, show warning and start fresh/backup

# On Exit:
#   # always prompt to save if there are unsaved changes
#   # write files and quit gracefully


# ==========================================
# MODULE 9: QUALITY + TESTING (adds hours)
# ==========================================

# Input Validation:
#   # central helper for safe integer input with ranges
#   # date parsing with friendly error messages
#   # confirmation prompts for destructive actions

# Unit Tests (simple):
#   # test scheduling math for flashcards (again/hard/good/easy)
#   # test add/update/delete task logic
#   # test stats computations (e.g., weekly totals)

# Sample Data Seeder:
#   # optional tool to generate N demo tasks/cards/pomodoros for testing

# Error Handling:
#   # try/catch around file IO
#   # fallback paths and user-friendly messages


# ==========================================
# STRETCH GOALS (pick a few to extend beyond 10 hours)
# ==========================================

# Stretch 1: Tag analytics
#   # show focus time per tag across tasks + pomodoros

# Stretch 2: Calendar export (iCal .ics)
#   # create events for due tasks or study blocks and write .ics file

# Stretch 3: Theming
#   # ASCII UI enhancements (borders, color if supported)

# Stretch 4: Notifications
#   # optional sound/beep or desktop notification hooks

# Stretch 5: Flashcard import from CSV/Anki-like format
#   # support basic fields and decks

# Stretch 6: Backup/Restore
#   # zip current JSON/CSV into a timestamped backup
#   # restore from chosen backup

# Stretch 7: Simple GUI later
#   # plan to port core logic into a GUI (Tkinter or web with Flask)
#   # keep logic modular so UI swap is easy

