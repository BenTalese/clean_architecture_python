from abc import ABC
from enum import Enum
import importlib
import inspect
import os
import sys
from Application.Infrastructure.Pipes.IBusinessRuleValidator import IBusinessRuleValidator
from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
from Application.Services.ITestService import ITestService
from Framework.Infrastructure.TestInfrastructure import TestInfrastructure
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from pprint import pprint

from typing import Dict, List, Type, Tuple
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator
from Application.Infrastructure.Pipes.IPipe import IPipe
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Domain.Errors.InterfaceNotImplementedError import InterfaceNotImplementedError

from Framework.Infrastructure.Persistence import Persistence

from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPortValidator import CreateTestEntityInputPortValidator
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Domain.Infrastructure.Generics import TInputPort, TInteractor, TOutputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter
import os
import sys

from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.Infrastructure.Pipeline.Wiring import Wiring
from Application.Infrastructure.Pipeline.UseCaseInvoker import UseCaseInvoker
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter


sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

# TODO: Pipes folder should be under services...I think, maybe also OutputPorts?

"""
IServiceCollectionExtensions
    ConfigureServices()
        CLAM.Register()
            ConfigurePipeline()
            ScanAssemblies()
            Validate()
"""

INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence),
    (ITestService, TestInfrastructure)
]

directory_exclusion_list = ["__pycache__"]
file_exclusion_list = ["__init__.py", "ICreateTestEntityOutputPort.py"]
di_scan_locations = ["Application/UseCases", "Framework/Infrastructure"]

_UseCaseScanLocations = ["Application/UseCases"]

#TODO: Point out to users that they can put everything together their own way if they don't want to use the built-in wiring and service provider
# For this i should define what they are required to do to hook things up and get it going
# Will need to point out conventions that make this work out of the box, e.g.
#   - DI_ for parameters
#   - One class per file for DI
#   - Class name matches module name
#   - Interfaces must be registered first (idk if i like this one...)

# TODO: Also, can demonstrate how you could have a "definitions.py" file with "ROOT_DIR = os.path.dirname(os.path.abspath(__file__))" that can be passed to scan everything...or maybe they can just pass "." ... not sure yet

_ServiceProvider = ServiceProvider()
Wiring.RegisterDependencies(_ServiceProvider, di_scan_locations, directory_exclusion_list, file_exclusion_list, INTERFACE_TO_CONCRETE)
_UseCaseRegistry = Wiring.ConstructUseCaseRegistry(_ServiceProvider, _UseCaseScanLocations, directory_exclusion_list, file_exclusion_list)
Wiring.RegisterPipeline(_ServiceProvider, _UseCaseRegistry)
invoker: UseCaseInvoker = Wiring.GetService(_ServiceProvider, UseCaseInvoker)
#ServiceProviderExtensions.ConfigureServices(_ServiceProvider, _UseCaseScanLocations, di_scan_locations, directory_exclusion_list, file_exclusion_list)

#invoker.Configure(_UseCaseScanLocations)





# Create the input and output ports
invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()


invoker.InvokeUseCase(invalid_input_port, output_port)



# Create and execute the pipeline for UseCase1
#pipeline = factory.create_pipeline("CreateTestEntity") # TODO: Change from getting pipeline by name to getting by InputPort from pipes registry
#pipeline.execute(invalid_input_port, output_port)

# Create and execute the pipeline for UseCase2
#pipeline = factory.create_pipeline("UseCase2")
#pipeline.execute(input_port, output_port)













"""
Options:
    - Only use type hints for finding dependencies (reduce readability)
  * - Use naming convention in parameters to identify dependencies e.g. "DI_<name>"
    - Decorate everything with "@injectable" and "@autowired" which ties the program to the "injectable" module
    - List out every single class and its dependencies (YUCK!)
    - Check against an exclusion list that I need to keep adding to
"""

#could get by name of module?... that would mean these would all need to be called by exact name, e.g. CreateTestEntityInputPortValidator instead of _createTestEntityInputPortValidator

"""
sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...
container = Container()
ContainerExtensions.Register(container, scan_locations, directory_exclusion_list, file_exclusion_list)
z = ContainerExtensions.GetService(Container, D)
xx = ContainerExtensions.GetService(container, Persistence) #DI_Persistence isn't there either??? just looking in debug mode
xxx = ContainerExtensions.GetService(container, CreateTestEntityInteractor)
xxxx = container.providers
v = 0


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
    def validate_pipeline():
        pass



"""


class UseCaseInvoker():
    def InvokeUseCase(inputPort: TInputPort, outputPort: TOutputPort):
        pass

class TestController():
    def __init__(self, useCaseInvoker: UseCaseInvoker):
        self._useCaseInvoker = useCaseInvoker

    def CreateTestEntity(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        self._useCaseInvoker.InvokeUseCase(inputPort, outputPort)
"""




"""
Style Guide

class: ExampleClass
method: ExampleMethod
parameter: exampleParameter
instance member: m_ExampleMember
local variable: _ExampleVariable
constant: EXAMPLE_CONSTANT
static member: s_ExampleMember

class: ExampleClass
method: example_method
parameter: example_parameter
instance member: _exampleMember
local variable: _ExampleVariable
constant: EXAMPLE_CONSTANT
static member: s_ExampleMember

"""
