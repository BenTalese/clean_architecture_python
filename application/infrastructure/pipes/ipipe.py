from abc import ABC, abstractmethod
from asyncio import Task
from typing import Callable, Coroutine, Generic
from application.infrastructure.pipeline.pipe_priority import PipePriority
from domain.infrastructure.generics import TInputPort, TOutputPort


class IPipe(Generic[TInputPort, TOutputPort], ABC):

    @property
    @abstractmethod
    def priority(self) -> PipePriority:
        pass


    @abstractmethod
    async def execute_async(self, input_port: TInputPort, output_port: TOutputPort) -> Coroutine | None:
        pass
