import ulid

def ulid_factory() -> str:
    return str(ulid.new())
