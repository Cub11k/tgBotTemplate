import copy


class BaseStorage:
    def __init__(self):
        self.data = {}

    def load(self):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError

    def set_data(self, **kwargs):
        updated = False
        for key, value in kwargs.items():
            if key not in self.data.keys() or self.data[key] != value:
                self.data[key] = copy.deepcopy(value)
                updated = True
        if updated:
            self.dump()

    def delete_data(self, *keys):
        for key in keys:
            if key in self.data.keys():
                del self.data[key]
            else:
                raise KeyError(key)
        self.dump()

    def get_data(self, *keys) -> tuple:
        result = []
        for key in keys:
            if key in self.data.keys():
                result.append(self.data[key])
            else:
                raise KeyError(key)
        return tuple(result)
