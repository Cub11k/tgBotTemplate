import os
import pickle
import atexit
from typing import Optional
from bot.storages.base_storage import BaseStorage


def create_dir(file_path):
    dirs = file_path.rsplit('/', maxsplit=1)[0]
    os.makedirs(dirs, exist_ok=True)
    if not os.path.isfile(file_path):
        with open(file_path, 'wb') as file:
            pickle.dump({}, file, protocol=pickle.HIGHEST_PROTOCOL)


class PickleStorage(BaseStorage):
    def __init__(self, file_path: Optional[str]):
        super().__init__()
        self.file_path = file_path if file_path is not None else "../.storages/data.pkl"
        create_dir(self.file_path)
        self.load()

        atexit.register(self.dump)

    def load(self):
        with open(self.file_path, 'rb') as file:
            self.data = pickle.load(file)

    def dump(self):
        with open(self.file_path, 'wb') as file:
            pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
