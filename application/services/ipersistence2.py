from typing import Protocol, TypeVar

TEntity = TypeVar("TEntity")

class IPersistence2(Protocol):

    def add(entity: TEntity) -> None:
        pass

    def remove(entity: TEntity) -> None:
        pass
