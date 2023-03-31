from abc import ABC, abstractmethod
from typing import Generic
from Domain.Infrastructure.Generics import TValidationFailure

class IValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    def PresentBusinessRuleValidationFailure(self, validationFailure: TValidationFailure) -> None:
        pass
    