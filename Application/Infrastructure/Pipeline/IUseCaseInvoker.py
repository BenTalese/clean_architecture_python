from abc import ABC, abstractmethod
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class IUseCaseInvoker(ABC):

    @abstractmethod
    def CanInvokeUseCase(self, inputPort: TInputPort, outputPort: TOutputPort) -> bool:
        pass


    @abstractmethod
    def InvokeUseCase(self, inputPort: TInputPort, outputPort: TOutputPort) -> None:
        pass
