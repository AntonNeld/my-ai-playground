import room

# Get stuff.


def get_view():
    to_return = {"score": room.get_current_room().score,
                 "steps": room.get_current_room().steps}
    serializables = []
    things = room.get_current_room().get_things()
    for thing in things:
        serializable = {"x":          thing.x,
                        "y":          thing.y,
                        "looks_like": thing.looks_like}
        serializables.append(serializable)

    to_return["things"] = serializables
    return to_return


def step():
    room.get_current_room().step()
