from collections.abc import MutableMapping


class PositionDict(MutableMapping):
    """Dict that also keeps a mapping from position to key"""

    def __init__(self, *args, **kwargs):
        self.positions = dict()
        self.keys_by_location = {}
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.positions[key]

    def __setitem__(self, key, value):
        if key in self.positions:
            self._remove_from_locations(key, self.positions[key])
        self.positions[key] = value
        self._add_to_locations(key, value)

    def __delitem__(self, key):
        value = self.positions[key]
        del self.positions[key]
        self._remove_from_locations(key, value)

    def __iter__(self):
        return iter(self.positions)

    def __len__(self):
        return len(self.positions)

    def _add_to_locations(self, key, value):
        x = value.x
        y = value.y
        if (x, y) not in self.keys_by_location:
            self.keys_by_location[(x, y)] = []
        self.keys_by_location[(x, y)].append(key)

    def _remove_from_locations(self, key, value):
        x = value.x
        y = value.y
        self.keys_by_location[(x, y)].remove(key)
        if len(self.keys_by_location[(x, y)]) == 0:
            del self.keys_by_location[(x, y)]

    def get_entities_at(self, x, y):
        try:
            return self.keys_by_location[(x, y)]
        except KeyError:
            return []
