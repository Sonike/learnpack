def can_edit(user: dict | None, note: dict) -> bool:
    """True if this user may edit this note. Deny unless a rule allows it."""
    # TODO: no user -> False; suspended -> False; admin -> True;
    #       member -> owns it and not locked; anything else -> False
    return True  # this is the bug: everyone can edit everything!


if __name__ == "__main__":
    print(can_edit({"id": 7, "role": "member"}, {"id": 3, "owner_id": 7}))   # True
    print(can_edit({"id": 7, "role": "member"}, {"id": 4, "owner_id": 8}))   # False
    print(can_edit(None, {"id": 3, "owner_id": 7}))                          # False
