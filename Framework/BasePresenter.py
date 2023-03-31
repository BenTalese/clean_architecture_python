from abc import ABC, abstractmethod
from Application.Infrastructure.OutputPorts.IValidationOutputPort import IValidationOutputPort
from Domain.Infrastructure.Generics import TValidationFailure


class BasePresenter(IValidationOutputPort, ABC):
    
    @abstractmethod
    def PresentValidationFailure(self, validationFailure: TValidationFailure) -> bool:
        print("Error!")
        