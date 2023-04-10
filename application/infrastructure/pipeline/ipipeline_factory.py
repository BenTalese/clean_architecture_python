from abc import ABC, abstractmethod
from typing import List, Type
from application.infrastructure.pipes.ipipe import IPipe
from domain.infrastructure.generics import TInputPort

class IPipelineFactory(ABC):

    @abstractmethod
    def create_pipeline(self, input_port: TInputPort) -> List[Type[IPipe]]:
        pass
