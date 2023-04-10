from abc import ABC, abstractmethod
from typing import Callable, Generic
from application.infrastructure.pipeline.pipe_priority import PipePriority
from domain.infrastructure.generics import TInputPort, TOutputPort


class IPipe(Generic[TInputPort, TOutputPort], ABC):

    @property
    @abstractmethod
    def priority(self) -> PipePriority:
        pass

    @abstractmethod
    def execute(self, input_port: TInputPort, output_port: TOutputPort) -> Callable | None:
        pass
