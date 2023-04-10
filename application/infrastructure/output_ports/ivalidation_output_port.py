from abc import ABC, abstractmethod
from typing import Generic
from domain.infrastructure.generics import TValidationFailure

class IValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    def present_validation_failure(self, validation_failure: TValidationFailure) -> None:
        pass
    