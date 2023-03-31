from abc import ABC, abstractmethod
from typing import Generic
from Domain.Infrastructure.Generics import TAuthorisationFailure

class IAuthorisationOutputPort(Generic[TAuthorisationFailure], ABC):
    
    @abstractmethod
    def PresentUnauthorised(self, authorisationFailure: TAuthorisationFailure) -> None:
        pass
    