
from abc import ABC
from application.infrastructure.pipeline.pipe_priority import PipePriority
from application.infrastructure.pipes.ipipe import IPipe


class IAuthenticationVerifier(IPipe, ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IAuthenticationVerifier
