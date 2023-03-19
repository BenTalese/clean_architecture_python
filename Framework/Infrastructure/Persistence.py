from Domain.Infrastructure.Generics import TEntity
from Application.Services.IPersistence import IPersistence


class Persistence(IPersistence):
    def Add(self, tEntity: TEntity) -> None:
        print("Added")

    def Remove(self, tEntity: TEntity) -> None:
        print("Removed")

    def SaveChanges(self) -> None:
        print("Saved")