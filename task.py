from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    title: str
    priority: int
    time_needed: int
    deadline: str

    def short_text(self) -> str:
        # короткая строка для вывода в меню
        return (
            f"{self.task_id}. {self.title} | приоритет: {self.priority} | "
            f"время: {self.time_needed} мин | дедлайн: {self.deadline}"
        )

    def copy(self) -> "Task":
        # делаем копию, чтобы отмена работала нормально
        return Task(self.task_id, self.title, self.priority, self.time_needed, self.deadline)
