from abc import ABC, abstractmethod
from application.infrastructure.output_ports.ivalidation_output_port import IValidationOutputPort
from domain.infrastructure.generics import TValidationFailure


class BasePresenter(IValidationOutputPort, ABC):
    
    @abstractmethod
    def present_validation_failure(self, validationFailure: TValidationFailure) -> bool:
        print("Error!")
        