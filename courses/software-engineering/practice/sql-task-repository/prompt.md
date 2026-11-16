# A task repository

Build `TaskRepository`: one class that owns all the SQL for a to-do app. The rest of the program will call its methods and get back `Task` objects, never tuples or SQL.

```python
@dataclass
class Task:
    id: int
    title: str
    status: str          # "todo" or "done"

class TaskRepository:
    def __init__(self, conn: sqlite3.Connection): ...
    def add(self, title: str) -> Task: ...
    def get(self, task_id: int) -> Task | None: ...
    def list(self, status: str | None = None) -> list[Task]: ...
    def complete(self, task_id: int) -> bool: ...
```

| Method | What it does |
|---|---|
| `__init__(conn)` | Keeps the connection and creates the `tasks` table if it doesn't exist: `id` INTEGER primary key, `title` TEXT required, `status` TEXT required, default `'todo'`. |
| `add(title)` | Strips spaces from both ends of `title`. If nothing is left, raises `ValueError`. Otherwise inserts a new task with status `"todo"`, commits, and returns it as a `Task` (with its new id). |
| `get(task_id)` | Returns that `Task`, or `None` if there's no such id. |
| `list(status=None)` | Returns all tasks ordered by id. If `status` is given (`"todo"` or `"done"`), only tasks with that status. |
| `complete(task_id)` | Sets the task's status to `"done"`, commits, and returns `True`. Returns `False` if there's no such task. |

**Every value must go through `?` parameters.** A test adds a task titled `x'); DROP TABLE tasks;--`. It must be stored as that exact text, and the table must still be there afterwards.

## Example

```python
repo = TaskRepository(sqlite3.connect(":memory:"))
repo.add("  Write tests  ")    # Task(id=1, title='Write tests', status='todo')
repo.add("Ship it")            # Task(id=2, title='Ship it', status='todo')
repo.complete(1)               # True
repo.list("done")              # [Task(id=1, title='Write tests', status='done')]
repo.get(99)                   # None
```
