import abc
from abc import abstractmethod


class BaseHandlers(abc.ABC):
    def __init__(self):
        pass

    @abstractmethod
    def register(self):
        raise NotImplementedError
