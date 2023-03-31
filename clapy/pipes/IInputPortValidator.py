from abc import ABC, abstractmethod
from typing import Generic
from Domain.Infrastructure.Generics import TInputPort, TOutputPort
from clapy.pipes.IPipe import IPipe
from clapy.pipes.PipePriority import PipePriority

class IInputPortValidator(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.InputPortValidator
