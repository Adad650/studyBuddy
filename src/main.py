import datetime



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

# Easter egg!!!
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







