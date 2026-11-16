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
        # TODO: a dict from id to Task works well, plus the next id to hand out
        pass

    def add(self, title: str) -> Task:
        """Create, store and return a new Task. Empty titles raise ValueError."""
        # TODO
        return Task(0, title)

    def complete(self, task_id: int) -> Task:
        """Mark a task DONE and return it. Unknown ids raise KeyError."""
        # TODO
        return Task(task_id, "?")

    def by_status(self, status: Status) -> list[Task]:
        """Tasks with this status, in the order they were added."""
        # TODO
        return []


if __name__ == "__main__":
    tasks = TaskList()
    tasks.add("Buy milk")
    tasks.add("Write tests")
    tasks.complete(1)
    print(tasks.by_status(Status.DONE))
    print(tasks.by_status(Status.TODO))
