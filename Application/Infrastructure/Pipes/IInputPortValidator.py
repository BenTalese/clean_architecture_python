from abc import ABC, abstractmethod
from typing import Generic
from ....Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IInputPortValidator(Generic[TInputPort, TOutputPort], ABC):
    
    @abstractmethod
    def Validate(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
    