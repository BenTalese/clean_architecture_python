from abc import ABC, abstractmethod
from typing import Generic
from domain.infrastructure.generics import TAuthorisationFailure

class IAuthorisationOutputPort(Generic[TAuthorisationFailure], ABC):
    
    @abstractmethod
    def present_unauthorised(self, authorisation_failure: TAuthorisationFailure) -> None:
        pass
    