from collections.abc import MutableMapping


class LabelDict(MutableMapping):
    """Dict that also keeps a mapping from label to key"""

    def __init__(self, *args, **kwargs):
        self.labels = dict()
        self.keys_by_label = dict()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.labels[key]

    def __setitem__(self, key, label):
        if key in self.labels and self.labels[key] == label:
            return
        if label in self.keys_by_label:
            raise RuntimeError(f"Entity with label {label} already exists")
        self.labels[key] = label
        self.keys_by_label[label] = key

    def __delitem__(self, key):
        label = self.labels[key]
        del self.labels[key]
        del self.keys_by_label[label]

    def __iter__(self):
        return iter(self.labels)

    def __len__(self):
        return len(self.labels)

    def get_entity_with_label(self, label):
        return self.keys_by_label[label]
