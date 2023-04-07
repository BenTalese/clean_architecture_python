from abc import ABC
import importlib
import inspect
import os
import re
import sys
from Application.Infrastructure.Pipeline.PipelineFactory import PipelineFactory
from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.Infrastructure.Pipeline.UseCaseInvoker import UseCaseInvoker
from Application.Infrastructure.Pipes.IPipe import IPipe
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Domain.Errors.InterfaceNotImplementedError import InterfaceNotImplementedError
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter
from dependency_injector import providers
from typing import Dict, List, Tuple, Type

sys.path.append(os.getcwd()) #TODO: fixes python unable to see Application.Infrastructure.etc...

class Wiring:

    @staticmethod
    def __GetServiceName(service: Type) -> str:
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            raise Exception(f"Could not detect class name from fully qualified name of {service}.")

        return _TypeMatch.group().replace('.', '_')


    @staticmethod
    def GetService(serviceProvider: ServiceProvider, service: Type) -> object:
        _ServiceName = Wiring.__GetServiceName(service)

        if _Service := serviceProvider.providers.get(_ServiceName):
            return _Service()
        else:
            raise Exception(f"Was not able to retrieve '{service.__name__}' from DI container.")


    # TODO: Register pipelinescanner as singleton
    # TODO: Register pipelinefactory as singleton
    # THIS SHOULD PROBABLY BE USER DEFINED, DON'T DO IT FOR THEM
    @staticmethod
    def ConstructServiceProvider( # BuildClapyEngine()? Wiring.BuildEngine()? ConfigureServices()?
        serviceProvider: ServiceProvider,
        usecase_scan_locations: List[str],
        scan_locations: List[str],
        directory_exclusion_list: List[str],
        file_exclusion_list: List[str]):
        pass


    # TODO: Currently this registers everything as a factory (need option to do singleton), could be added to interface registry?
    @staticmethod
    def RegisterDependencies(
        serviceProvider: ServiceProvider,
        scanLocations: List[str],
        directoryExclusionList: List[str],
        fileExclusionList: List[str],
        interfaceRegistry: List[Tuple[type, type]]):

        for _Location in scanLocations:
            for _Root, _Directories, _Files in os.walk(_Location):
                _Directories[:] = [d for d in _Directories if d not in directoryExclusionList]
                _Files[:] = [f for f in _Files if f not in fileExclusionList]
                for _File in _Files:
                    _ModuleName = _File[:-3]
                    _Module = importlib.import_module(f"{_Root.replace('/', '.')}.{_ModuleName}", package=None)
                    _ModuleClass = getattr(_Module, _ModuleName, None)

                    if _ModuleClass is None:
                        raise Exception(f"""Could not find class for '{_ModuleName}'. Classes must be named the same as their module to be registered
                        in the dependency container. If you do not want this module to be scanned, add it to the file exclusions.""")

                    _ClassToRegister = Wiring.__TryGetConcreteImplementation(_ModuleClass, interfaceRegistry)

                    Wiring.RegisterDependency(serviceProvider, _ClassToRegister)

        v = Wiring.GetService(serviceProvider, CreateTestEntityInteractor)
        valid_input_port = CreateTestEntityInputPort("Hello")
        output_port = CreateTestEntityPresenter()
        v.Execute(valid_input_port, output_port)
        vb = 0


    @staticmethod
    def __TryGetConcreteImplementation(classType: Type, interfaceRegistry: List[Tuple[type, type]]) -> object:
        _IsInterface = ABC in classType.__bases__

        if _IsInterface:
            if classType not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
                raise LookupError(f"Interface '{classType.__name__}' does not have a concrete class registered.")

            return [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == classType][0]

        return classType


    @staticmethod
    def RegisterDependency(serviceProvider: ServiceProvider, classType: Type) -> object:
        _DependencyName = Wiring.__GetServiceName(classType)

        if hasattr(serviceProvider, _DependencyName):
            print(f"Skipped registering {_DependencyName} of type {classType} because container already has {_DependencyName} registered.")
            return getattr(serviceProvider, _DependencyName)

        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(classType.__init__).parameters.items()
                                            if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]

        if not _DependencyParametersFromConstructor:
            setattr(serviceProvider, _DependencyName, providers.Factory(classType))
            return getattr(serviceProvider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(Wiring.RegisterDependency(serviceProvider, _Dependency.annotation))

        setattr(serviceProvider, _DependencyName, providers.Factory(classType, *_SubDependencies))

        return getattr(serviceProvider, _DependencyName)


    # TODO: Pipeline priority passed in, also this might be good as separate methods... maybe?
    @staticmethod
    def RegisterPipeline(serviceProvider: ServiceProvider, useCaseRegistry: Dict[str, List[Type[IPipe]]]):
        _FactoryRegistrationName = Wiring.__GetServiceName(PipelineFactory)

        if hasattr(serviceProvider, _FactoryRegistrationName):
            print(f"Skipped registering PipelineFactory because container already has one registered.")
            return #TODO: probably don't just return

        setattr(serviceProvider, _FactoryRegistrationName, providers.Singleton(PipelineFactory, pipeRegistry=useCaseRegistry))

        _Factory = getattr(serviceProvider, _FactoryRegistrationName)

        _InvokerRegistrationName = Wiring.__GetServiceName(UseCaseInvoker)

        #TODO: this is repeating code
        if hasattr(serviceProvider, _InvokerRegistrationName):
            print(f"Skipped registering PipelineFactory because container already has one registered.")
            return #TODO: probably don't just return
        
        setattr(serviceProvider, _InvokerRegistrationName, providers.Factory(UseCaseInvoker, pipelineFactory=_Factory))

    @staticmethod
    def ConstructUseCaseRegistry(
        serviceProvider: ServiceProvider,
        useCaseLocations: List[str],
        directoryExclusionList: List[str], # TODO: make exclusion lists optional
        fileExclusionList: List[str]) -> Dict[str, List[Type[IPipe]]]:

        _UseCaseRegistry = {}

        #TODO: this is repeating code "go through these locations and get the files excluding particular files/folders"
        for _Location in useCaseLocations:
            for _Root, _Directories, _Files in os.walk(_Location):
                _Directories[:] = [d for d in _Directories if d not in directoryExclusionList]
                _Files[:] = [f for f in _Files if f not in fileExclusionList]

                _Pipes = []

                for _File in _Files:
                    _ModuleName = _File[:-3]
                    _Module = importlib.import_module(f"{_Root.replace('/', '.')}.{_ModuleName}", package=None)
                    _ModuleClass = getattr(_Module, _ModuleName, None)
                    if issubclass(_ModuleClass, IPipe):
                        try:
                            _Pipes.append(Wiring.GetService(serviceProvider, _ModuleClass))
                        except TypeError:
                            raise InterfaceNotImplementedError(_ModuleName)
                if _Pipes:
                    _UseCaseRegistry[_Root.replace('/', '.')] = { "pipes": _Pipes }
                    #pipes_registry[root.split("/")[-1]] = { "pipes": pipes }
                    #pipes_registry[os.path.basename(dirpath)] = {"interactor": CreateTestEntityInteractor(Persistence()), "pipes": pipes}

        return _UseCaseRegistry
