import room

# Get stuff.


def get_view():
    return room.get_current_room().get_view()


def step():
    room.get_current_room().step()


def reset():
    room.init_room()
