from abc import ABC
from enum import Enum
import importlib
import inspect
import os
import sys
from Application.Infrastructure.Pipes.IBusinessRuleValidator import IBusinessRuleValidator
from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
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

"""
Options:
    - Only use type hints for finding dependencies (reduce readability)
  * - Use naming convention in parameters to identify dependencies e.g. "DI_<name>"
    - Decorate everything with "@injectable" and "@autowired" which ties the program to the "injectable" module
    - List out every single class and its dependencies (YUCK!)
    - Check against an exclusion list that I need to keep adding to
"""

#could get by name of module?... that would mean these would all need to be called by exact name, e.g. CreateTestEntityInputPortValidator instead of _createTestEntityInputPortValidator

container = Container()
ContainerExtensions.Register(container, scan_locations, directory_exclusion_list, file_exclusion_list)
z = ContainerExtensions.GetService(Container, D)
xx = ContainerExtensions.GetService(container, Persistence) #DI_Persistence isn't there either??? just looking in debug mode
xxx = ContainerExtensions.GetService(container, CreateTestEntityInteractor)
xxxx = container.providers
v = 0
"""
container = Container()

x = container.C()
z = container.get_instance(C)
z = container.GetService(C)
"""


"""
# module.py
from dependency_injector import containers, providers
import os

class MyContainer(containers.DeclarativeContainer):
    def __init__(self):
        super().__init__()

        # Automatically scan and load modules
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith('.py') and file != '__init__.py':
                module_name = os.path.splitext(file)[0]
                ######################################          module = __import__(f'.{module_name}', fromlist=[None])
                for name in dir(module):
                    obj = getattr(module, name)
                    if hasattr(obj, '__dependencies__'):
                        dependencies = obj.__dependencies__
                        setattr(self, name, providers.Factory(obj, *dependencies))

"""

"""
Storage Options:
    1. Pipe priority stored against the specific pipe interface
    2. Pipe priority stored in a priority file, similar to here

    #Sort in factory
"""

class PipelineValidator:
    @staticmethod
    def ValidatePipeline():
        pass







"""
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
"""
