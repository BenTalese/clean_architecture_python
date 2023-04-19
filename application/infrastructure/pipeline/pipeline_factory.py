from typing import Dict, List, Type
from application.infrastructure.pipeline.common import _import_class_by_namespace
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iservice_provider import IServiceProvider
from application.infrastructure.pipes.ipipe import IPipe
from domain.infrastructure.generics import TInputPort

class PipelineFactory(IPipelineFactory):
    
    def __init__(self, service_provider: IServiceProvider, usecase_registry: Dict[str, List[Type[IPipe]]]):
        self._service_provider = service_provider if service_provider is not None else ValueError(f"'{service_provider=}' cannot be None.")
        self._usecase_registry = usecase_registry if usecase_registry is not None else ValueError(f"'{usecase_registry=}' cannot be None.")


    def create_pipeline(self, input_port: TInputPort) -> List[Type[IPipe]]:
        _UsecaseKey = input_port.__module__.rsplit(".", 1)[0]

        if _UsecaseKey not in self._usecase_registry:
            raise KeyError(f"Could not find '{input_port}' in the pipeline registry.")
        
        _PipeNamespaces = self._usecase_registry[_UsecaseKey]["pipes"]

        _PipeClasses = [_import_class_by_namespace(_Namespace) for _Namespace in _PipeNamespaces]

        _Pipes = [self._service_provider.get_service(_PipeClass) for _PipeClass in _PipeClasses]
        
        return sorted(_Pipes, key=lambda _Pipe: _Pipe.priority)
