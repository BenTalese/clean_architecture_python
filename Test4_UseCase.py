from abc import ABCMeta, abstractmethod
from typing import TypeVar

TEntity = TypeVar("TEntity")

class IPersistence(metaclass=ABCMeta):
    @abstractmethod
    def Add(self) -> None:
        pass

class Persistence(IPersistence):
    def Add(self) -> None:
        print(1)

class Interactor():
    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def handle(self):
        self._persistence.Add()

Interactor(Persistence()).handle()