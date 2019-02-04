
def get_coordinates(percept, target):
    targets = [thing for thing in percept["things"]
               if thing["looks_like"] == target]
    x = [thing["x"] for thing in targets]
    y = [thing["y"] for thing in targets]
    return set(zip(x, y))
