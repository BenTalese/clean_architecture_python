from abc import ABC, abstractmethod
from typing import Callable, Generic
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Domain.Infrastructure.Generics import TInputPort, TOutputPort


class IPipe(Generic[TInputPort, TOutputPort], ABC):

    @property
    @abstractmethod
    def Priority(self) -> PipePriority:
        pass

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> Callable:
        pass
