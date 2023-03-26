from abc import ABC, abstractmethod
from Application.Infrastructure.Pipeline.PipePriority import PriorityEnum
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IInteractor(IPipe, ABC):

    @property
    def Priority(self) -> PriorityEnum:
        return PriorityEnum.Interactor

    @abstractmethod
    def Execute(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass
    