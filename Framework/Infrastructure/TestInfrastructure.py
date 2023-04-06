from Application.Services.ITestService import ITestService
from Domain.Infrastructure.Generics import TEntity


class TestInfrastructure(ITestService):
    def Add(self, tEntity: TEntity) -> None:
        print("Added")

    def Remove(self, tEntity: TEntity) -> None:
        print("Removed")

    def SaveChanges(self) -> None:
        print("Saved")
