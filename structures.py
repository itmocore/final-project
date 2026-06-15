from typing import Optional

from task import Task


class TaskQueue:
    def __init__(self) -> None:
        self._items: list[int] = []

    def enqueue(self, task_id: int) -> None:
        # добавляем задачу в очередь
        self._items.append(task_id)

    def dequeue(self):
        # забираем первую задачу
        if not self._items:
            return None
        return self._items.pop(0)

    def remove_task_id(self, task_id: int) -> None:
        # убираем удалённую задачу из очереди
        self._items = [item for item in self._items if item != task_id]

    def items(self) -> list[int]:
        return list(self._items)


class UndoStack:
    def __init__(self) -> None:
        self._items: list[tuple[list[Task], list[int], int]] = []

    def push(self, tasks: list[Task], queue: list[int], next_id: int) -> None:
        # сохраняем состояние перед изменением
        self._items.append(([task.copy() for task in tasks], list(queue), next_id))

    def pop(self):
        # достаём последний снимок
        if not self._items:
            return None
        return self._items.pop()


class TreeNode:
    def __init__(self, task: Task) -> None:
        self.deadline = task.deadline
        self.tasks = [task]
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None


def insert_task(root: Optional[TreeNode], task: Task) -> TreeNode:
    # обычное дерево поиска по дедлайну
    if root is None:
        return TreeNode(task)
    if task.deadline < root.deadline:
        root.left = insert_task(root.left, task)
    elif task.deadline > root.deadline:
        root.right = insert_task(root.right, task)
    else:
        root.tasks.append(task)
    return root


def build_tree(tasks: list[Task]) -> Optional[TreeNode]:
    # строим дерево из списка задач
    root = None
    for task in tasks:
        root = insert_task(root, task)
    return root


def inorder(root: Optional[TreeNode]) -> list[Task]:
    # рекурсивный обход слева направо
    if root is None:
        return []
    return inorder(root.left) + root.tasks + inorder(root.right)


def find_min(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # ищем самый ранний дедлайн
    if root is None:
        return None
    while root.left is not None:
        root = root.left
    return root


def find_max(root: Optional[TreeNode]) -> Optional[TreeNode]:
    # ищем самый поздний дедлайн
    if root is None:
        return None
    while root.right is not None:
        root = root.right
    return root
