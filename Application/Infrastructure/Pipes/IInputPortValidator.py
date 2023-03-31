from abc import ABC, abstractmethod
from typing import Generic
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IInputPortValidator(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.InputPortValidator
