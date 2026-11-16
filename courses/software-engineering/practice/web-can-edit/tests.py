from solution import can_edit

ADA = {"id": 7, "role": "member"}
TUNDE = {"id": 8, "role": "member"}
ADMIN = {"id": 1, "role": "admin"}
ADAS_NOTE = {"id": 3, "owner_id": 7}


def check(user, note, want):
    got = can_edit(user, note)
    assert got is want, f"can_edit({user!r}, {note!r}): expected {want!r}, got {got!r}"


def test_owner_can_edit_their_own_note():
    check(ADA, ADAS_NOTE, True)
    check(ADA, {"id": 9, "owner_id": 7, "locked": False}, True)


def test_member_cannot_edit_someone_elses_note():
    check(TUNDE, ADAS_NOTE, False)


def test_admin_can_edit_any_note_even_locked():
    check(ADMIN, ADAS_NOTE, True)
    check(ADMIN, {"id": 4, "owner_id": 8, "locked": True}, True)


def test_locked_note_blocks_its_owner():
    check(ADA, {"id": 3, "owner_id": 7, "locked": True}, False)


def test_nobody_logged_in_or_suspended_cannot_edit():
    check(None, ADAS_NOTE, False)
    check({"id": 7, "role": "suspended"}, ADAS_NOTE, False)


def test_unknown_roles_are_denied():
    check({"id": 7, "role": "superuser"}, ADAS_NOTE, False)
    check({"id": 7}, ADAS_NOTE, False)
