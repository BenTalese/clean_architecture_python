from abc import ABC, abstractmethod
from domain.infrastructure.generics import TEntity


class IPersistence(ABC):

    @abstractmethod
    def add(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    def remove(self, entity: TEntity) -> None:
        pass

    @abstractmethod
    def save_changes(self) -> None:
        pass
