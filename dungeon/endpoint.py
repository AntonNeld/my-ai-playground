import room

# Get stuff.


def get_view():
    serializables = []
    things = room.get_current_room().get_things()
    for thing in things:
        serializable = {"x":          thing.x,
                        "y":          thing.y,
                        "looks_like": thing.looks_like}
        serializables.append(serializable)
    return serializables


def step():
    room.get_current_room().step()
