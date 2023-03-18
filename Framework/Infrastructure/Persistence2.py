from typing import TypeVar

TEntity = TypeVar("TEntity")

class Persistence2():

    def Add(tEntity: TEntity) -> None:
        print(3)

    def Remove(tEntity: TEntity) -> None:
        print(4)