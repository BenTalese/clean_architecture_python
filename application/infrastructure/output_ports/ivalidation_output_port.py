from abc import ABC, abstractmethod
from asyncio import Task
from typing import Generic
from domain.infrastructure.generics import TValidationFailure

class IValidationOutputPort(Generic[TValidationFailure], ABC):
    
    @abstractmethod
    async def present_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
        pass
    