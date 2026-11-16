def can_edit(user: dict | None, note: dict) -> bool:
    """True if this user may edit this note. Deny unless a rule allows it."""
    if user is None:
        return False
    role = user.get("role")
    if role == "admin":
        return True
    if role == "member":
        return note["owner_id"] == user["id"] and not note.get("locked", False)
    return False  # suspended, unknown or missing roles


if __name__ == "__main__":
    print(can_edit({"id": 7, "role": "member"}, {"id": 3, "owner_id": 7}))
