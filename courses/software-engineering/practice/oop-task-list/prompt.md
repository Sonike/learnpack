# A task list with a dataclass and an Enum

Model a to-do list using `@dataclass` for the data and an `Enum` for the fixed set of statuses.

```python
class Status(Enum):
    TODO = "todo"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    status: Status = Status.TODO

class TaskList:
    def __init__(self): ...
    def add(self, title: str) -> Task: ...
    def complete(self, task_id: int) -> Task: ...
    def by_status(self, status: Status) -> list[Task]: ...
```

- `Status` and `Task` are written for you in the starter. Keep them as they are.
- `add(title)` creates a `Task` with the next id (the first task gets `1`, then `2`, and so on), stores it, and returns it. An empty or whitespace-only title raises `ValueError`.
- `complete(task_id)` sets that task's status to `Status.DONE` and returns the task. An id that doesn't exist raises `KeyError`.
- `by_status(status)` returns the tasks with that status, in the order they were added.

## Example

```python
tasks = TaskList()
tasks.add("Buy milk")        # Task(id=1, title='Buy milk', status=<Status.TODO: 'todo'>)
tasks.add("Write tests")     # Task(id=2, ...)
tasks.complete(1)
tasks.by_status(Status.DONE) # [Task(id=1, title='Buy milk', status=<Status.DONE: 'done'>)]
tasks.complete(99)           # KeyError
```
