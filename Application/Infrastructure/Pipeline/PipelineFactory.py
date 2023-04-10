from typing import Dict, List, Type
from Application.Infrastructure.Pipeline.IPipelineFactory import IPipelineFactory
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort

class PipelineFactory(IPipelineFactory):
    
    def __init__(self, useCaseRegistry: Dict[str, List[Type[IPipe]]]):
        self.__useCaseRegistry = useCaseRegistry if useCaseRegistry is not None else ValueError(f"'{useCaseRegistry=}' cannot be None.")


    def CreatePipeline(self, inputPort: TInputPort) -> List[Type[IPipe]]:
        _UseCaseKey = inputPort.__module__.rsplit(".", 1)[0]

        if _UseCaseKey not in self.__useCaseRegistry:
            raise KeyError(f"Could not find '{inputPort}' in the pipeline registry.")
        
        _Pipes = self.__useCaseRegistry[_UseCaseKey]["pipes"]
        
        #TODO: This feels like a weird check to have...
        if any(_Pipe is None for _Pipe in _Pipes):
            raise Exception(f"One of the pipes for the use case '{_UseCaseKey}' is not configured correctly.")
        
        _SortedPipes = sorted(_Pipes, key=lambda _Pipe: _Pipe.Priority)
        return _SortedPipes
