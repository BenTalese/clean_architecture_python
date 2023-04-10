from abc import ABC, abstractmethod
from domain.infrastructure.generics import TInputPort, TOutputPort

class IUseCaseInvoker(ABC):

    @abstractmethod
    def can_invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        pass


    @abstractmethod
    def invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        pass
