from abc import ABC, abstractmethod
from typing import Generic

from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IPipe(Generic[TInputPort, TOutputPort], ABC):
    
    @property
    @abstractmethod
    def Priority(self) -> int:
        pass

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
