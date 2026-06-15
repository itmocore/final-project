from task import Task
from structures import TaskQueue, UndoStack, build_tree, find_max, find_min, inorder
from helpers import check_deadline


class TaskManager:
    def __init__(self) -> None:
        # тут храним всё состояние программы
        self.tasks: list[Task] = []
        self.queue = TaskQueue()
        self.undo_stack = UndoStack()
        self.next_id = 1

    def _find_index(self, task_id: int) -> int:
        # ищем задачу по номеру
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                return index
        return -1

    def _push_state(self) -> None:
        # сохраняем снимок перед изменениями
        self.undo_stack.push(self.tasks, self.queue.items(), self.next_id)

    def find_task_by_id(self, task_id: int):
        index = self._find_index(task_id)
        if index == -1:
            return None
        return self.tasks[index]

    def add_task(self, title: str, priority: int, time_needed: int, deadline: str) -> str:
        if not check_deadline(deadline):
            return "неверный формат дедлайна. используйте гггг-мм-дд."

        self._push_state()
        self.tasks.append(Task(self.next_id, title, priority, time_needed, deadline))
        self.next_id += 1
        return "задача добавлена."

    def edit_task(self, task_id: int, title: str, priority: int, time_needed: int, deadline: str) -> str:
        index = self._find_index(task_id)
        if index == -1:
            return "задача не найдена."
        if not check_deadline(deadline):
            return "неверный формат дедлайна. используйте гггг-мм-дд."

        self._push_state()
        task = self.tasks[index]
        task.title = title
        task.priority = priority
        task.time_needed = time_needed
        task.deadline = deadline
        return "задача изменена."

    def delete_task(self, task_id: int) -> str:
        index = self._find_index(task_id)
        if index == -1:
            return "задача не найдена."

        self._push_state()
        self.tasks.pop(index)
        self.queue.remove_task_id(task_id)
        return "задача удалена."

    def add_to_queue(self, task_id: int) -> str:
        if self._find_index(task_id) == -1:
            return "задача не найдена."
        self.queue.enqueue(task_id)
        return "задача добавлена в очередь."

    def execute_next_task(self) -> str:
        task_id = self.queue.dequeue()
        if task_id is None:
            return "очередь пуста."

        task = self.find_task_by_id(task_id)
        if task is None:
            return f"задача {task_id} была удалена, поэтому пропущена."
        return f"выполнена задача: {task.short_text()}"

    def undo_last_action(self) -> str:
        state = self.undo_stack.pop()
        if state is None:
            return "нечего отменять."

        tasks, queue, next_id = state
        self.tasks = [task.copy() for task in tasks]
        self.queue = TaskQueue()
        for item in queue:
            self.queue.enqueue(item)
        self.next_id = next_id
        return "последнее действие отменено."

    def show_all_tasks(self) -> str:
        if not self.tasks:
            return "список задач пуст."
        return "\n".join(task.short_text() for task in self.tasks)

    def show_queue(self) -> str:
        items = self.queue.items()
        if not items:
            return "очередь пуста."

        lines = ["очередь задач:"]
        for task_id in items:
            task = self.find_task_by_id(task_id)
            if task is None:
                lines.append(f"{task_id}. [задача удалена]")
            else:
                lines.append(task.short_text())
        return "\n".join(lines)

    def show_by_deadline(self) -> str:
        root = build_tree(self.tasks)
        ordered = inorder(root)
        if not ordered:
            return "список задач пуст."
        return "\n".join(task.short_text() for task in ordered)

    def show_earliest(self) -> str:
        root = build_tree(self.tasks)
        node = find_min(root)
        if node is None:
            return "список задач пуст."
        return "\n".join(task.short_text() for task in node.tasks)

    def show_latest(self) -> str:
        root = build_tree(self.tasks)
        node = find_max(root)
        if node is None:
            return "список задач пуст."
        return "\n".join(task.short_text() for task in node.tasks)
