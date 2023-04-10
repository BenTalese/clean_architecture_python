from typing import TypeVar

TEntity = TypeVar("TEntity")

class Persistence2():

    def add(entity: TEntity) -> None:
        print(3)

    def remove(entity: TEntity) -> None:
        print(4)
