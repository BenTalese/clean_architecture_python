from abc import ABC
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Application.Infrastructure.Pipes.IPipe import IPipe

class IEntityExistenceChecker(IPipe, ABC):
    
    @property
    def CanInvokeNextPipe(self) -> bool:
        return self.m_CanInvokeNextPipe
        #return not self._failures
    
    @property
    def Priority(self) -> PipePriority:
        return PipePriority.EntityExistenceChecker
