from abc import ABC
import importlib
import inspect
import os
import sys
from Application.Infrastructure.Pipes.IBusinessRuleValidator import IBusinessRuleValidator
from Application.Infrastructure.Pipes.IInteractor import IInteractor
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from pprint import pprint

from typing import Dict, List, Type, Tuple
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator
from Application.Infrastructure.Pipes.IPipe import IPipe
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Domain.Errors.InterfaceNotImplementedError import InterfaceNotImplementedError

from Framework.Infrastructure.Persistence import Persistence
sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPortValidator import CreateTestEntityInputPortValidator
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Domain.Infrastructure.Generics import TInputPort, TInteractor, TOutputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    Persistence = providers.Object(Persistence)
    CreateTestEntityInteractor = providers.Factory(CreateTestEntityInteractor, persistence=Persistence) #will need a scanner too
    CreateTestEntityInputPortValidator = providers.Factory(CreateTestEntityInputPortValidator)
#could get by name of module?... that would mean these would all need to be called by exact name, e.g. CreateTestEntityInputPortValidator instead of _createTestEntityInputPortValidator

container = Container()

"""
Storage Options:
    1. Pipe priority stored against the specific pipe interface
    2. Pipe priority stored in a priority file, similar to here

    #Sort in factory
"""
PIPE_PRIORITY: List[Tuple[Type[IPipe], int]] = [
    (IInputPortValidator, 1),
    (IBusinessRuleValidator, 2),
    (IInteractor, 3)
]

class PipelineValidator:
    @staticmethod
    def ValidatePipeline():
        pass

class Pipeline:
    def __init__(self, pipes: List[IInputPortValidator]):
        self.pipes = pipes

    def execute(self, input_port: IInputPort, output_port: TOutputPort):
        for pipe in self.pipes:
            pipe.Execute(input_port, output_port)


class PipelineFactory:
    def __init__(self, pipes_registry):
        self.pipes_registry = pipes_registry

    def create_pipeline(self, use_case_name):
        #pipes = [self.pipes_registry[p] for p in self.pipes_registry if p in use_case_name]
        pipes = self.pipes_registry[use_case_name]["pipes"]
        sorted_pipes = sorted(pipes, key=lambda pipe: next(order[1] for order in PIPE_PRIORITY if isinstance(pipe, order[0])))
        sorted_pipes2 = sorted(pipes, key=lambda p: p.Priority)
        return Pipeline(sorted_pipes)

class PipelineScanner:
    def __init__(self, parent_use_case_folder_path: str):
        self._parent_use_case_folder_path = parent_use_case_folder_path

    test2 = os.path.dirname(os.path.realpath(__file__)) #'/home/benny/Repos/clean_architecture_python/Application/Infrastructure/Pipeline' (could set globally...)

    def scan(self) -> Dict[str, List[Type[IPipe]]]:
        pipes_registry = {}
        for root, dirs, files in os.walk(self._parent_use_case_folder_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__") #also could do for file... if file.endswith(".py")
            pipes = []
            for file in files:
                module_name = file[:-3]
                module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}", package=None)
                obj = getattr(module, module_name, None)
                #obj = container.get_provider(klass)()
                if issubclass(obj, IPipe):
                    try:
                        #pipes.append(container.providers.get(obj))
                        x = container.providers.get(module_name)
                        pipes.append(x())
                    except TypeError:
                        raise InterfaceNotImplementedError(module_name)
            if pipes.__len__() > 0:
                pipes_registry[root.split("/")[-1]] = {"interactor": CreateTestEntityInteractor(Persistence()), "pipes": pipes}
                #pipes_registry[os.path.basename(dirpath)] = {"interactor": CreateTestEntityInteractor(Persistence()), "pipes": pipes}

        #pprint(pipes_registry)

        return pipes_registry
    
pipes_registry = PipelineScanner("Application/UseCases").scan()

# Create the pipeline factory with the pipes registry
factory = PipelineFactory(pipes_registry)

# Create the input and output ports
invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()

# Create and execute the pipeline for UseCase1
pipeline = factory.create_pipeline("CreateTestEntity")
pipeline.execute(invalid_input_port, output_port)

# Create and execute the pipeline for UseCase2
#pipeline = factory.create_pipeline("UseCase2")
#pipeline.execute(input_port, output_port)

class UseCaseInvoker():
    def InvokeUseCase(inputPort: TInputPort, outputPort: TOutputPort):
        pass

class TestController():
    def __init__(self, useCaseInvoker: UseCaseInvoker):
        self._useCaseInvoker = useCaseInvoker

    def CreateTestEntity(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        self._useCaseInvoker.InvokeUseCase(inputPort, outputPort)
