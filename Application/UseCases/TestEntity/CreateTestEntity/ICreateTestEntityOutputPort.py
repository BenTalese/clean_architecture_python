from abc import ABC, abstractmethod
from typing import List

from Application.Dtos.TestDto import TestDto
from clapy.outputports.IValidationOutputPort import IValidationOutputPort

# IAuthenticationOutputPort, IAuthorisationOutputPort, IBusinessRuleValidationOutputPort (maybe not necessary having last one)
class ICreateTestEntityOutputPort(IValidationOutputPort, ABC):
    
    @abstractmethod
    def PresentTest(self, dto: TestDto) -> None:
        pass
