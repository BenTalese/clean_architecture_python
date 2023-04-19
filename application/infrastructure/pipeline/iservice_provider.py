from abc import ABC, abstractmethod
from typing import Type

from domain.infrastructure.generics import TServiceType


class IServiceProvider(ABC):

    @abstractmethod
    def get_service(self, service: Type[TServiceType]) -> TServiceType:
        pass
