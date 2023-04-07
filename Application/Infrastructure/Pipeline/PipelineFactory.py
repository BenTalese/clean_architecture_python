from typing import Dict, List, Type
from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.Infrastructure.Pipes.IPipe import IPipe


class PipelineFactory:
    def __init__(self, pipeRegistry: Dict[str, List[Type[IPipe]]]):
        self.m_PipeRegistry = pipeRegistry

    def create_pipeline(self, inputPort: IInputPort) -> List[Type[IPipe]]:
        usecase_key = inputPort.__module__.rsplit(".", 1)[0]

        if usecase_key not in self.m_PipeRegistry:
            raise KeyError(f"Could not find '{inputPort}' in the pipeline registry.")
        
        pipes = self.m_PipeRegistry[usecase_key]["pipes"]
        
        if pipes is None:
            raise Exception(f"Pipeline registry for '{inputPort}' contained no pipes.")
        
        if any(pipe is None for pipe in pipes):
            raise Exception(f"One of the pipes for the use case '{usecase_key}' is not configured correctly.")
        
        sorted_pipes = sorted(pipes, key=lambda pipe: pipe.Priority)
        return sorted_pipes
