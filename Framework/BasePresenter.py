from abc import ABC, abstractmethod
from clapy.outputports.IValidationOutputPort import IValidationOutputPort
from Domain.Infrastructure.Generics import TValidationFailure


class BasePresenter(IValidationOutputPort, ABC):
    
    @abstractmethod
    def PresentValidationFailure(self, validationFailure: TValidationFailure) -> bool:
        print("Error!")
        