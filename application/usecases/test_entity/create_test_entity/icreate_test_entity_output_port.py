from abc import ABC, abstractmethod
from Application.Dtos.TestDto import TestDto
from Application.Infrastructure.OutputPorts.IValidationOutputPort import IValidationOutputPort
from Application.Infrastructure.OutputPorts.IAuthorisationOutputPort import IAuthorisationOutputPort

class ICreateTestEntityOutputPort(IAuthorisationOutputPort, IValidationOutputPort, ABC):
    
    @abstractmethod
    def PresentTest(self, dto: TestDto) -> None:
        pass
