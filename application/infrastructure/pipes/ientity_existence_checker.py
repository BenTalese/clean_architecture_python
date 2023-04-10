from abc import ABC
from typing import Generic
from application.infrastructure.pipeline.pipe_priority import PipePriority
from application.infrastructure.pipes.ipipe import IPipe
from domain.infrastructure.generics import TInputPort, TOutputPort

class IEntityExistenceChecker(IPipe, Generic[TInputPort, TOutputPort], ABC):
    
    @property
    def priority(self) -> PipePriority:
        return PipePriority.IEntityExistenceChecker
