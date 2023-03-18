from typing import Protocol, TypeVar

TEntity = TypeVar("TEntity")

class IPersistence2(Protocol):

    def Add(tEntity: TEntity) -> None:
        pass

    def Remove(tEntity: TEntity) -> None:
        pass