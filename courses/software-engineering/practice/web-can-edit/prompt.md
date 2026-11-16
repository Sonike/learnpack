# Who may edit this note?

The most common serious bug in real APIs is **broken access control**: user 7 changes the id in the URL and edits user 8's data. Write the authorisation rule for a notes app as one small function that every edit handler calls.

```python
def can_edit(user: dict | None, note: dict) -> bool: ...
```

- `user`: the logged-in user, like `{"id": 7, "role": "member"}`, or `None` if nobody is logged in. `role` is `"admin"`, `"member"` or `"suspended"`.
- `note`: the note being edited, like `{"id": 3, "owner_id": 7, "locked": False}`.

Rules, in order:

1. Nobody logged in (`user` is `None`) → `False`.
2. A `"suspended"` user can't edit anything, not even their own notes → `False`.
3. An `"admin"` can edit any note, even a locked one → `True`.
4. A `"member"` can edit a note only if they own it (`note["owner_id"] == user["id"]`) **and** it isn't locked → `True`.
5. Anything else → `False`. This includes roles you don't recognise: **deny unless allowed**.

`note` may not have a `"locked"` key; treat that as not locked (`note.get("locked", False)`).

## Example

```python
can_edit({"id": 7, "role": "member"}, {"id": 3, "owner_id": 7})   # True
can_edit({"id": 7, "role": "member"}, {"id": 4, "owner_id": 8})   # False: someone else's note
can_edit({"id": 1, "role": "admin"},  {"id": 4, "owner_id": 8, "locked": True})   # True
can_edit(None, {"id": 3, "owner_id": 7})                          # False
```
