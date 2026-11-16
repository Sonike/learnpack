from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    TODO = "todo"
    DONE = "done"


@dataclass
class Task:
    id: int
    title: str
    status: Status = Status.TODO


class TaskList:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str) -> Task:
        """Create, store and return a new Task. Empty titles raise ValueError."""
        if not title.strip():
            raise ValueError("title cannot be empty")
        task = Task(self._next_id, title)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> Task:
        """Mark a task DONE and return it. Unknown ids raise KeyError."""
        task = self._tasks[task_id]  # raises KeyError for an unknown id
        task.status = Status.DONE
        return task

    def by_status(self, status: Status) -> list[Task]:
        """Tasks with this status, in the order they were added."""
        return [task for task in self._tasks.values() if task.status == status]


if __name__ == "__main__":
    tasks = TaskList()
    tasks.add("Buy milk")
    tasks.complete(1)
    print(tasks.by_status(Status.DONE))
