from abc import ABC, abstractmethod
from typing import List

from Application.Dtos.TestDto import TestDto
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator


class ICreateTestEntityOutputPort(IInputPortValidator, ABC):
    
    @abstractmethod
    def PresentTest(self, dto: TestDto) -> None:
        pass

    @abstractmethod
    def PresentValidationFailures(self, failures: List[str]) -> None:
        pass
