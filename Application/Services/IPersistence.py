from abc import ABCMeta, abstractmethod
from typing import TypeVar

TEntity = TypeVar("TEntity")

class IPersistence(metaclass=ABCMeta):

    @abstractmethod
    def Add(tEntity: TEntity) -> None:
        pass

    @abstractmethod
    def Add(tEntity: TEntity) -> None:
        pass