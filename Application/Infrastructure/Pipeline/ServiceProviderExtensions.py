from abc import ABC
import importlib
import inspect
import os
import re
import sys
from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter
from dependency_injector import providers
from typing import List, Tuple, Type

sys.path.append(os.getcwd()) #TODO: fixes python unable to see Application.Infrastructure.etc...

class ServiceProviderExtensions: # TODO: Rename to Wiring or something

    @staticmethod
    def __GetServiceName(service: Type) -> str:
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            raise Exception(f"Could not detect class name from fully qualified name of {service}.")
        
        return _TypeMatch.group().replace('.', '_')

    @staticmethod
    def GetService(serviceProvider: ServiceProvider, service: Type) -> object:
        _ServiceName = ServiceProviderExtensions.__GetServiceName(service)

        if _Service := serviceProvider.providers.get(_ServiceName):
            return _Service()
        else:
            raise Exception(f"Was not able to retrieve '{service.__name__}' from DI container.")

    # TODO: Register pipelinescanner as singleton
    # TODO: Register pipelinefactory as singleton
    @staticmethod
    def ConstructServiceProvider( # BuildClapyEngine()? Wiring.BuildEngine()?
        serviceProvider,
        usecase_scan_locations: List[str],
        scan_locations: List[str],
        directory_exclusion_list: List[str],
        file_exclusion_list: List[str]): #ConfigureServices():
        pass

    # TODO: Separate this into different methods
    # TODO: Add ability for user to specify "pls scan everything", which may take the form of "*" in the location list or an empty list
    # TODO: Currently this registers everything as a factory (need option to do singleton)
    @staticmethod
    def RegisterDependencies(
        serviceProvider: ServiceProvider,
        scanLocations: List[str],
        directoryExclusionList: List[str],
        fileExclusionList: List[str],
        interfaceRegistry: List[Tuple[type, type]]): #TODO: type hint this

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

                    ServiceProviderExtensions.RegisterDependency(serviceProvider, _ModuleClass, interfaceRegistry)


    #ImplementationProvider class?
    #Could have CheckIfInterface()?
    @staticmethod
    def __TryGetConcreteImplementation():
        pass

    @staticmethod
    def RegisterDependency(serviceProvider: ServiceProvider, classType: Type, interfaceRegistry: List[Tuple[type, type]]):
        _IsInterface = ABC in classType.__bases__

        if _IsInterface:
            if classType not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
                raise LookupError(f"Interface '{classType.__name__}' does not have a concrete class registered.")

            classType = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == classType][0]

        _DependencyName = ServiceProviderExtensions.__GetServiceName(classType)

        if hasattr(serviceProvider, _DependencyName):
            print(f"Skipped registering {_DependencyName} of type {classType} because container already has {_DependencyName} registered.")
            return getattr(serviceProvider, _DependencyName) #TODO: perhaps this should raise an exception because you shouldn't have two classes with the same namespace

        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(classType.__init__).parameters.items()
                                            if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]

        if not _DependencyParametersFromConstructor:
            setattr(serviceProvider, _DependencyName, providers.Factory(classType))
            return getattr(serviceProvider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(ServiceProviderExtensions.RegisterDependency(serviceProvider, _Dependency.annotation, interfaceRegistry))

        setattr(serviceProvider, _DependencyName, providers.Factory(classType, *_SubDependencies))

        return getattr(serviceProvider, _DependencyName)
    

    @staticmethod
    def RegisterPipeline(): #enum thing?
        pass


    @staticmethod
    def ConfigurePipelineScanner():
        pass


    @staticmethod
    def ConfigurePipelineFactory():
        pass
