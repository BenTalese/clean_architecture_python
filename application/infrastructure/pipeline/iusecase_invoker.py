from abc import ABC, abstractmethod
from domain.infrastructure.generics import TInputPort, TOutputPort

class IUseCaseInvoker(ABC):

    @abstractmethod
    async def invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        pass
