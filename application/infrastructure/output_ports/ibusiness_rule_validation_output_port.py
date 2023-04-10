from abc import ABC, abstractmethod
from typing import Generic
from domain.infrastructure.generics import TValidationFailure

class IBusinessRuleValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    def present_business_rule_validation_failure(self, validation_failure: TValidationFailure) -> None:
        pass
    