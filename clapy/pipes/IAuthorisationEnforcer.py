from abc import ABC
from typing import Generic
from Domain.Infrastructure.Generics import TInputPort, TOutputPort
from clapy.pipes.IPipe import IPipe
from clapy.pipes.PipePriority import PipePriority

class IAuthorisationEnforcer(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.AuthorisationEnforcer
