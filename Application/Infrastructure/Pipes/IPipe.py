from abc import ABC, abstractmethod
from typing import Generic
from Application.Infrastructure.Pipeline.PipePriority import PriorityEnum

from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IPipe(Generic[TInputPort, TOutputPort], ABC):
    
    @property
    @abstractmethod
    def Priority(self) -> PriorityEnum:
        pass

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
