
from abc import ABC, abstractmethod
from asyncio import Task

from application.infrastructure.output_ports.ivalidation_output_port import IValidationOutputPort


class IAsyncOutputPort(IValidationOutputPort, ABC):
    
    @abstractmethod
    async def present_test_async(self, text: int, order: int) -> None:
        pass
