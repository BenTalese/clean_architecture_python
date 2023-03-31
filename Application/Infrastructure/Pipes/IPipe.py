from abc import ABC, abstractmethod
from typing import Generic
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IPipe(Generic[TInputPort, TOutputPort], ABC):

    def __init__(self):
        self.m_CanInvokeNextPipe = True

    @property
    def CanInvokeNextPipe(self) -> bool:
        return self.m_CanInvokeNextPipe
    
    @property
    @abstractmethod
    def Priority(self) -> PipePriority:
        pass

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
