# Score a resume bullet

Recruiters skim a resume in seconds. Each bullet under a project or job should start with a strong **action verb**, show a **number** (users, speed, size, coverage), and fit on one or two lines. "Responsible for…" describes a duty, not a result.

Write `score_resume_bullet(text: str) -> list[str]` that returns a list of problems, in this order, using these exact strings:

1. `"no action verb"`: the first word (lower-cased, with trailing punctuation removed) is not in `ACTION_VERBS` (given in the starter).
2. `"no number"`: the bullet contains no digit.
3. `"responsible for"`: the bullet contains the phrase "responsible for" (any case).
4. `"too long"`: the bullet is over 200 characters (roughly two lines on a one-page resume).

Before checking, strip spaces and any leading bullet marker (`-`, `*` or `•`). A strong bullet returns `[]`.

## Examples

```python
score_resume_bullet("- Built a FastAPI service with 14 endpoints and 92% test coverage")
# []
score_resume_bullet("Responsible for the backend of a group project")
# ['no action verb', 'no number', 'responsible for']
score_resume_bullet("Worked on tests")
# ['no action verb', 'no number']
```
