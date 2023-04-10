from abc import ABC, abstractmethod
from typing import List, Type
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort

class IPipelineFactory(ABC):

    @abstractmethod
    def CreatePipeline(self, inputPort: TInputPort) -> List[Type[IPipe]]:
        pass
