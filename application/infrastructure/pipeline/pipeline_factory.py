from typing import Dict, List, Type
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipes.ipipe import IPipe
from domain.infrastructure.generics import TInputPort

class PipelineFactory(IPipelineFactory):
    
    def __init__(self, usecase_registry: Dict[str, List[Type[IPipe]]]):
        self._usecaseRegistry = usecase_registry if usecase_registry is not None else ValueError(f"'{usecase_registry=}' cannot be None.")


    def create_pipeline(self, input_port: TInputPort) -> List[Type[IPipe]]:
        _UsecaseKey = input_port.__module__.rsplit(".", 1)[0]

        if _UsecaseKey not in self._usecaseRegistry:
            raise KeyError(f"Could not find '{input_port}' in the pipeline registry.")
        
        _Pipes = self._usecaseRegistry[_UsecaseKey]["pipes"]
        
        return sorted(_Pipes, key=lambda _Pipe: _Pipe.priority)
