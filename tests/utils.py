from uuid import UUID, uuid4


def uuid_generate() -> UUID:
    # Note: Work around UUIDs with leading zeros:
    # https://github.com/tiangolo/sqlmodel/issues/25
    # by making sure uuid str does not start with a leading 0
    val = uuid4()
    while val.hex[0] == "0":
        val = uuid4()
    return val
