from abc import ABC, abstractmethod
from typing import Generic

from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IBusinessRuleValidator(IPipe, Generic[TInputPort, TOutputPort], ABC):

    @abstractmethod
    def Validate(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
    