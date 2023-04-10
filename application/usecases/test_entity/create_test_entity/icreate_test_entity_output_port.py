from abc import ABC, abstractmethod
from application.dtos.test_dto import TestDto
from application.infrastructure.output_ports.iauthorisation_output_port import IAuthorisationOutputPort
from application.infrastructure.output_ports.ivalidation_output_port import IValidationOutputPort

class ICreateTestEntityOutputPort(IAuthorisationOutputPort, IValidationOutputPort, ABC):
    
    @abstractmethod
    def present_test(self, dto: TestDto) -> None:
        pass
