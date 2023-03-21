from abc import ABC, abstractmethod
from typing import List

from Application.Dtos.TestDto import TestDto
from Application.Infrastructure.OutputPorts.IValidationOutputPort import IValidationOutputPort
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator

# IAuthenticationOutputPort, IAuthorisationOutputPort, IBusinessRuleValidationOutputPort (maybe not necessary having last one)
class ICreateTestEntityOutputPort(IValidationOutputPort, ABC):
    
    @abstractmethod
    def PresentTest(self, dto: TestDto) -> None:
        pass
