
from abc import ABC
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Application.Infrastructure.Pipes.IPipe import IPipe


class IAuthenticationVerifier(IPipe, ABC):
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.Authentication
