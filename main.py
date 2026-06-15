from helpers import read_deadline, read_int
from manager import TaskManager


def print_menu() -> None:
    print("\n=== Система управления задачами с приоритетами ===")
    print("1. добавить задачу")
    print("2. показать все задачи")
    print("3. изменить задачу")
    print("4. удалить задачу")
    print("5. добавить задачу в очередь")
    print("6. показать очередь")
    print("7. выполнить следующую задачу")
    print("8. показать задачи по дедлайну")
    print("9. показать самую раннюю задачу")
    print("10. показать самую позднюю задачу")
    print("11. отменить последнее действие")
    print("0. выход")


def main() -> None:
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("выберите пункт: ").strip()

        if choice == "1":
            title = input("название задачи: ").strip()
            priority = read_int("приоритет (1 — самый высокий): ")
            time_needed = read_int("время выполнения в минутах: ")
            deadline = read_deadline()
            print(manager.add_task(title, priority, time_needed, deadline))

        elif choice == "2":
            print(manager.show_all_tasks())

        elif choice == "3":
            task_id = read_int("номер задачи: ")
            title = input("новое название: ").strip()
            priority = read_int("новый приоритет: ")
            time_needed = read_int("новое время выполнения в минутах: ")
            deadline = read_deadline()
            print(manager.edit_task(task_id, title, priority, time_needed, deadline))

        elif choice == "4":
            task_id = read_int("номер задачи для удаления: ")
            print(manager.delete_task(task_id))

        elif choice == "5":
            task_id = read_int("номер задачи для очереди: ")
            print(manager.add_to_queue(task_id))

        elif choice == "6":
            print(manager.show_queue())

        elif choice == "7":
            print(manager.execute_next_task())

        elif choice == "8":
            print(manager.show_by_deadline())

        elif choice == "9":
            print(manager.show_earliest())

        elif choice == "10":
            print(manager.show_latest())

        elif choice == "11":
            print(manager.undo_last_action())

        elif choice == "0":
            print("выход из программы.")
            break

        else:
            print("некорректный пункт меню.")


if __name__ == "__main__":
    main()
