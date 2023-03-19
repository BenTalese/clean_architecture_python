from abc import ABC, abstractmethod
from ....Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IInteractor(ABC):

    @abstractmethod
    def Handle(self, inputPort: TInputPort, outputPort: TOutputPort) -> None:
        pass
    