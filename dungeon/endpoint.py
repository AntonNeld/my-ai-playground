from room import default_room

# Get stuff.
def get_view():
    serializables = []
    things = default_room.get_things()
    for thing in things:
        serializable = {"x":          thing.x,
                        "y":          thing.y,
                        "looks_like": thing.looks_like}
        serializables.append(serializable)
    return serializables

def step():
    print("Did a step!")