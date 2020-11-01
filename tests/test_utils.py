from uuid import UUID


def is_uuid(string):
    try:
        UUID(hex=string)
        return True
    except (ValueError, TypeError):
        return False


def test_helper_is_uuid():
    assert is_uuid("9f4118fe668843a3a1c847552a69b1db")
    assert not is_uuid("banana")
