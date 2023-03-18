from Application.Services import IPersistence
from typing import TypeVar

TEntity = TypeVar("TEntity")

class Persistence(IPersistence):

    def Add(tEntity: TEntity) -> None:
        print(1)

    def Remove(tEntity: TEntity) -> None:
        print(2)