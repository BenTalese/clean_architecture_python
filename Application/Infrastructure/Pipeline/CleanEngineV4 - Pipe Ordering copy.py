from abc import ABC
from enum import Enum
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

class A(ABC):
    pass

class B(A):
    pass

class C():
    def __init__(self, b: B) -> None:
        self._b = b

class D():
    pass

"""
Options:
    - Only use type hints for finding dependencies (reduce readability)
  * - Use naming convention in parameters to identify dependencies e.g. "DI_<name>"
    - Decorate everything with "@injectable" and "@autowired" which ties the program to the "injectable" module
    - List out every single class and its dependencies (YUCK!)
    - Check against an exclusion list that I need to keep adding to
"""

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    Persistence = providers.Object(Persistence)
    CreateTestEntityInteractor = providers.Factory(CreateTestEntityInteractor, persistence=Persistence) #will need a scanner too
    CreateTestEntityInputPortValidator = providers.Factory(CreateTestEntityInputPortValidator)
    B = providers.Factory(B)
    C = providers.Factory(C, b = B)

    instance = None

    def __init__(self, scan_locations):
        #super().__init__()
        Container.instance = self
        self._scan_locations = scan_locations

    scan_locations = ["Application/UseCases", "Framework/Infrastructure"]



    def get_instance(self, cls):
        return self.get(cls)()
            


#could get by name of module?... that would mean these would all need to be called by exact name, e.g. CreateTestEntityInputPortValidator instead of _createTestEntityInputPortValidator

container = Container()
#container.Register()

class ContainerExtensions():

    @staticmethod
    def GetService(container: Container, service):
        try:
            x = container.providers.get(service.__name__)()
            return x
        except Exception as e:
            print(f"Was not able to retrive {service.__name__} from DI container. (Original exception: {e}.)")

    @staticmethod
    def Register(container: Container, scan_locations: List[str], directory_exclusion_list: List[str], file_exclusion_list: List[str]):
        for path in scan_locations:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in directory_exclusion_list]
                files[:] = [f for f in files if f not in file_exclusion_list]
                for file in files:
                    module_name = file[:-3]
                    module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}", package=None)
                    obj = getattr(module, module_name, None)
                    params = inspect.signature(obj.__init__).parameters
                    dependencies = []
                    for name, param in params.items(): #if not kwargs, not args, not self, 
                        if (param.annotation != inspect.Parameter.empty
                            and inspect.isclass(param.annotation) #this won't stop classes being registered when they should be passed in
                            and name not in container.providers): # name or param.name might not work... e.g. container has "Example" where parameter is named "example"
                            dependencies.append(name, param.annotation) #probably this will append a camel-case name...
                    if dependencies:
                        dependency_dict = {
                            name: getattr(container, cls.__name__) for name, cls in dependencies
                        }
                        setattr(
                            container,
                            module_name,
                            providers.Factory(module, kwargs=dependency_dict)
                        )
                        for dependency_name, dependency_obj in dependencies:
                            setattr(container, dependency_name, dependency_obj)
                    setattr(container, module_name, providers.Factory(module, )) # this also won't work if the class to be registered does not match file name

directory_exclusion_list = ["__pycache__"]
file_exclusion_list = ["__init__.py"]

x = container.C()
z = ContainerExtensions.GetService(Container, D)
print(x)
print(z)
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
PIPE_PRIORITY: List[Tuple[Type[IPipe], int]] = [
    (IInputPortValidator, 1),
    (IBusinessRuleValidator, 2),
    (IInteractor, 3)
]

class PriorityEnum(Enum):
    InputPortValidator = 1
    BusinessRuleValidator = 2
    Interactor = 3

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
