from abc import ABC, abstractmethod

from Domain.Infrastructure.Generics import TEntity

class ITestService(ABC):

    @abstractmethod
    def Add(self, tEntity: TEntity) -> None:
        pass

    @abstractmethod
    def Remove(self, tEntity: TEntity) -> None:
        pass

    @abstractmethod
    def SaveChanges(self) -> None:
        pass
