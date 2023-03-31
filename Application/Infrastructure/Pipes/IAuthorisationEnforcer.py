from abc import ABC
from typing import Generic
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IAuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.AuthorisationEnforcer