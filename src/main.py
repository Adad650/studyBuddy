from datetime import datetime
import curses


TASK_TEMPLATE = {
    "title": "",
    "details": "",
    "dueDate": None,
    "priority": None,
    "tags": [],
    "status": "todo",
    "createdAt": None,
    "completedAt": None,
    "flashCards": []
}

tasks = []

def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting…")
        exit()

def prompt_int(prompt, valid=None):
    while True:
        s = safe_input(prompt).strip()
        try:
            val = int(s)
            if valid and val not in valid:
                print(f"Enter one of: {valid}")
                continue
            return val
        except ValueError:
            print("Enter a valid integer.")

def prompt_datetime(prompt):
    s = safe_input(prompt + " (YYYY-MM-DD HH:MM or blank): ").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Invalid format. Use YYYY-MM-DD HH:MM")
        return prompt_datetime(prompt)

def fmt_dt(dt):
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "N/A"

def resolve_task_selection(task_list, selection):
    if not task_list:
        return None
    sel = selection.strip()
    if sel.isdigit():
        idx = int(sel) - 1
        if 0 <= idx < len(task_list):
            return task_list[idx]
        return None
    low = sel.lower()
    for t in task_list:
        if str(t.get("title", "")).strip().lower() == low:
            return t
    return None

def format_task_output(task, detailed=False):
    priority_map = {1: "High", 2: "Medium", 3: "Low"}
    tags_str = ", ".join(task["tags"]) if task["tags"] else "No tags"

    lines = [
        f"Task: {task.get('title', 'Untitled Task')}",
        f"Status: {str(task.get('status', 'N/A')).upper()}",
        f"Due: {fmt_dt(task['dueDate'])}",
        f"Priority: {priority_map.get(task.get('priority'), 'Not set')}",
        f"Tags: {tags_str}",
        f"Details: {task.get('details', 'No details provided')}",
        f"Created: {fmt_dt(task['createdAt'])}",
        f"Completed: {fmt_dt(task['completedAt'])}",
    ]

    if detailed and task.get("flashCards"):
        lines.append("Flashcards:")
        for i, card in enumerate(task["flashCards"], start=1):
            title = card.get("Title", "Untitled")
            text = card.get("Text", "No content")
            lines.append(f"  {i}. {title} -> {text}")

    return "\n".join(lines)

def listTaskBrief(ts):
    if not ts:
        print("No tasks found.")
        return
    for i, t in enumerate(ts, start=1):
        status = str(t.get('status', 'N/A')).upper()
        title = str(t.get('title', 'Untitled'))
        due_disp = fmt_dt(t['dueDate']) if t['dueDate'] else "No due date"
        print(f"{i}. {title} [{status}] (Due: {due_disp})")

def create_task():
    task = TASK_TEMPLATE.copy()
    task["title"] = safe_input("Task name: ").strip()
    task["details"] = safe_input("Description: ").strip()
    task["dueDate"] = prompt_datetime("Due date")
    task["priority"] = prompt_int("Priority (1=high, 2=medium, 3=low): ", valid=[1, 2, 3])
    tags_raw = safe_input("Tags (comma separated): ").strip()
    task["tags"] = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
    task["status"] = safe_input("Status (todo/doing/done): ").strip().lower() or "todo"
    task["createdAt"] = datetime.now()

    n = prompt_int("How many flash cards? (0+): ")
    for i in range(n):
        print(f"Flashcard {i+1}")
        card_title = safe_input("  Title: ").strip()
        card_text = safe_input("  Answer: ").strip()
        task["flashCards"].append({"Title": card_title, "Text": card_text})

    return task

def edit_task(task):
    while True:
        print(f"Editing {task.get('title', 'Untitled')}")
        choice = prompt_int(
            "1. Title\n2. Details\n3. Due Date\n4. Priority\n5. Tags\n6. Status\n7. Flashcards\n8. Back\n",
            valid=[1,2,3,4,5,6,7,8]
        )
        match choice:
            case 1:
                task["title"] = safe_input("New title: ").strip()
            case 2:
                task["details"] = safe_input("New details: ").strip()
            case 3:
                task["dueDate"] = prompt_datetime("New due date")
            case 4:
                task["priority"] = prompt_int("New priority (1=high, 2=medium, 3=low): ", valid=[1,2,3])
            case 5:
                tags_raw = safe_input("New tags (comma separated): ").strip()
                task["tags"] = [t.strip() for t in tags_raw.split(",")] if tags_raw else []
            case 6:
                task["status"] = safe_input("New status (todo/doing/done): ").strip().lower() or task.get("status","todo")
                if task["status"] == "done":
                    task["completedAt"] = datetime.now()
            case 7:
                manage_flashcards(task)
            case 8:
                break

def manage_flashcards(task):
    cards = task.get("flashCards", [])
    while True:
        sub = prompt_int("1. List\n2. Add\n3. Edit\n4. Delete\n5. Back\n", valid=[1,2,3,4,5])
        if sub == 1:
            if not cards:
                print("No flashcards.")
            else:
                for i, card in enumerate(cards, start=1):
                    print(f"{i}. {card.get('Title','Untitled')} -> {card.get('Text','')}")
        elif sub == 2:
            title = safe_input("Title: ").strip()
            text = safe_input("Answer: ").strip()
            cards.append({"Title": title, "Text": text})
        elif sub == 3:
            if not cards:
                print("No flashcards.")
                continue
            for i, card in enumerate(cards, start=1):
                print(f"{i}. {card.get('Title','Untitled')} -> {card.get('Text','')}")
            idx = prompt_int("Select card to edit: ")
            if 1 <= idx <= len(cards):
                cards[idx-1]["Title"] = safe_input("New title: ").strip()
                cards[idx-1]["Text"] = safe_input("New answer: ").strip()
        elif sub == 4:
            if not cards:
                print("No flashcards.")
                continue
            for i, card in enumerate(cards, start=1):
                print(f"{i}. {card.get('Title','Untitled')} -> {card.get('Text','')}")
            idx = prompt_int("Select card to delete: ")
            if 1 <= idx <= len(cards):
                cards.pop(idx-1)
        elif sub == 5:
            return

def viewTaskDetail(ts):
    if not ts:
        print("No tasks available.")
        return
    listTaskBrief(ts)
    sel = safe_input("Task number or name: ").strip()
    t = resolve_task_selection(ts, sel)
    if t:
        print(format_task_output(t, detailed=True))
    else:
        print("Task not found.")

def studyMode(task_list):
    if not task_list:
        print("No tasks to study.")
        return
    listTaskBrief(task_list)
    sel = safe_input("Task number or name: ").strip()
    chosen_task = resolve_task_selection(task_list, sel)
    if not chosen_task:
        print("Task not found.")
        return
    cards = chosen_task.get("flashCards", [])
    if not cards:
        print("This task has no flashcards.")
        return
    print(f"Studying {chosen_task.get('title')}")
    score = 0
    for i, card in enumerate(cards, start=1):
        q = card.get("Title", f"Card {i}")
        a = card.get("Text", "")
        print(f"Q{i}: {q}")
        user_answer = safe_input("Your answer: ").strip()
        if user_answer.lower() == a.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong. Answer: {a}")
    print(f"Score: {score}/{len(cards)}")

def main(stdscr):
    index = 0
    menu_labels = [
        "Add Task",
        "View All",
        "View One",
        "Edit",
        "Study Mode",
        "Exit"
    ]
    while True:
        curses.curs_set(0)
        stdscr.erase()
        stdscr.addstr(0, 0, "Study Buddy")
        for i, label in enumerate(menu_labels):
            style = curses.A_REVERSE if i == index else curses.A_NORMAL
            stdscr.addstr(2 + i, 2, f"{i+1}. {label}", style)
        stdscr.refresh()
        key = stdscr.getch()

        if key in (curses.KEY_UP, ord('k')):
            index = (index - 1) % len(menu_labels)
        elif key in (curses.KEY_DOWN, ord('j')):
            index = (index + 1) % len(menu_labels)
        elif key in (curses.KEY_ENTER, 10, 13):
            if index == 0:
                curses.endwin()
                new_task = create_task()
                if new_task:
                    tasks.append(new_task)
                    print("Task created.")
                input("Press Enter to continue...")
                stdscr.clear()
            elif index == 1:
                curses.endwin()
                listTaskBrief(tasks)
                input("Press Enter to continue...")
                stdscr.clear()
            elif index == 2:
                curses.endwin()
                viewTaskDetail(tasks)
                input("Press Enter to continue...")
                stdscr.clear()
            elif index == 3:
                curses.endwin()
                if not tasks:
                    print("No tasks.")
                else:
                    listTaskBrief(tasks)
                    idx = prompt_int("Task number to edit: ")
                    if 1 <= idx <= len(tasks):
                        edit_task(tasks[idx-1])
                input("Press Enter to continue...")
                stdscr.clear()
            elif index == 4:
                curses.endwin()
                studyMode(tasks)
                input("Press Enter to continue...")
                stdscr.clear()
            elif index == 5:
                curses.endwin()
                print("Goodbye!")
                break

    while True:
        choice = prompt_int("1. Add Task\n2. View All\n3. View One\n4. Edit\n5. Study Mode\n6. Exit\n", valid=[1,2,3,4,5,6])
        match choice:
            case 1:
                new_task = create_task()
                if new_task:
                    tasks.append(new_task)
                    print("Task created.")
            case 2:
                listTaskBrief(tasks)
            case 3:
                viewTaskDetail(tasks)
            case 4:
                if not tasks:
                    print("No tasks.")
                else:
                    listTaskBrief(tasks)
                    idx = prompt_int("Task number to edit: ")
                    if 1 <= idx <= len(tasks):
                        edit_task(tasks[idx-1])
            case 5:
                studyMode(tasks)
            case 6:
                print("Goodbye!")
                break
            case _:
                print("Invalid choice.")

if __name__ == "__main__":
    curses.wrapper(main)
