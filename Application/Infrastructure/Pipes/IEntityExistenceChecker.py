from abc import ABC, abstractmethod
from typing import Generic

from Application.Infrastructure.Pipes.IPipe import IPipe
from ....Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IEntityExistenceChecker(IPipe, Generic[TInputPort, TOutputPort], ABC):

    @property
    def Priority(self) -> int:
        return 0
    
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> TOutputPort:
        return super().Execute(inputPort, outputPort)
    
    @abstractmethod
    def DoesEntityExist(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        pass
    