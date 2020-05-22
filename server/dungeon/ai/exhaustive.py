from dungeon.ai.lib.perception import get_coordinates
from dungeon.ai.lib.pathfinding import breadth_first


class ExhaustiveAI:

    def __init__(self):
        self._plan = []

    def next_move(self, percept):
        print("Starting up!")

        if not self._plan:
            walls = get_coordinates(percept, "wall")
            coins = get_coordinates(percept, "coin")

            distances = {}
            pos = list(coins) + [(0, 0)]

            for coin in pos:
                for coin2 in pos:
                    if coin is not coin2:
                        distances[(coin, coin2)] = breadth_first(
                            coin, coin2, walls)

            self._plan = _helper((0, 0), coins, [], None, walls, distances)

        return self._plan.pop(0)

    def to_json(self):
        return "exhaustive"


def _helper(pos, coins, path, bestpath, walls, distances):
    print("Pos: " + str(pos) + "     Coins left: " + str(len(coins)))

    if coins is None or len(coins) == 0:
        return []

    if len(coins) == 1:
        # print("End of the line")
        (coin,) = coins
        return path + distances[(pos, coin)]

    for coin in coins:
        p = path + distances[(pos, coin)]
        if bestpath is not None and len(p) >= len(bestpath):
            # print("This path stinks!")
            continue
        p2 = _helper(coin, coins.difference(
            [coin]), p, bestpath, walls, distances)

        if bestpath is None or len(bestpath) > len(p2):
            bestpath = p2

    return bestpath
