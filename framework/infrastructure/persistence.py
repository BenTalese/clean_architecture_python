from Application.Services.ITestService import ITestService
from Domain.Infrastructure.Generics import TEntity
from Application.Services.IPersistence import IPersistence


class Persistence(IPersistence):
    def __init__(self, DI_Test: ITestService):
        self._test = DI_Test
    
    def Add(self, tEntity: TEntity) -> None:
        self._test.Add(tEntity)
        print("Added")

    def Remove(self, tEntity: TEntity) -> None:
        print("Removed")

    def SaveChanges(self) -> None:
        print("Saved")
