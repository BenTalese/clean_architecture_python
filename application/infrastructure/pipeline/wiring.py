from abc import ABC
import importlib
import inspect
import os
import re
from Application.Infrastructure.Pipeline.PipePriority import PipePriority
from Application.Infrastructure.Pipeline.PipelineFactory import PipelineFactory
from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.Infrastructure.Pipeline.UseCaseInvoker import UseCaseInvoker
from Application.Infrastructure.Pipes.IAuthenticationVerifier import IAuthenticationVerifier
from Application.Infrastructure.Pipes.IAuthorisationEnforcer import IAuthorisationEnforcer
from Application.Infrastructure.Pipes.IBusinessRuleValidator import IBusinessRuleValidator
from Application.Infrastructure.Pipes.IEntityExistenceChecker import IEntityExistenceChecker
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator
from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Errors.InterfaceNotImplementedError import InterfaceNotImplementedError
from dependency_injector import providers
from typing import Dict, List, Optional, Tuple, Type


#TODO: find a place for this to live
DIR_EXCLUSIONS = [r"__pycache__"]
FILE_EXCLUSIONS = [r".*__init__\.py", r".*OutputPort\.py"]


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


    # TODO: Currently this registers everything as a factory (need option to do singleton), could be added to interface registry?
    # TODO: ^^^ This problem would be solved by manual service registration, so not what this is which is Clapy-Auto
    @staticmethod
    def RegisterDependencies(
        serviceProvider: ServiceProvider,
        interfaceRegistry: List[Tuple[type, type]],
        dependencyScanLocations: Optional[List[str]] = ["."],
        directoryExclusionPatterns: Optional[List[str]] = [],
        fileExclusionPatterns: Optional[List[str]] = []):

        directoryExclusionPatterns = directoryExclusionPatterns + DIR_EXCLUSIONS
        fileExclusionPatterns = fileExclusionPatterns + FILE_EXCLUSIONS

        for _Location in dependencyScanLocations:
            for _Root, _Directories, _Files in os.walk(_Location):
                for _ExclusionPattern in directoryExclusionPatterns:
                    _Directories[:] = [d for d in _Directories if not re.match(_ExclusionPattern, d)]

                for _ExclusionPattern in fileExclusionPatterns:
                    _Files[:] = [f for f in _Files if not re.match(_ExclusionPattern, f)]

                for _File in _Files:
                    _Namespace = _Root.replace('/', '.') + "." + _File[:-3]
                    _Class = Wiring.ImportClassByNamespace(_Namespace)

                    Wiring.RegisterDependency(serviceProvider, _Class, interfaceRegistry)


    @staticmethod
    def __TryGetConcreteImplementation(classType: Type, interfaceRegistry: List[Tuple[type, type]]) -> object:
        _IsInterface = ABC in classType.__bases__

        if _IsInterface:
            if classType not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
                raise LookupError(f"Interface '{classType.__name__}' does not have a concrete class registered.")

            return [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == classType][0]

        return classType


    # TODO: Currently parameters will always be registered as factories, also the module itself will also always be a factory
    # TODO: Something to think about, could use parameter name to determine factory or singleton, e.g. "DI_S_" is singleton, "DI_F_" is factory
    @staticmethod
    def RegisterDependency(
        serviceProvider: ServiceProvider,
        classType: Type,
        interfaceRegistry: List[Tuple[type, type]],
        providerMethod: Optional[Type] = providers.Factory) -> object:

        _ClassToRegister = Wiring.__TryGetConcreteImplementation(classType, interfaceRegistry)
        _DependencyName = Wiring.__GetServiceName(_ClassToRegister)

        if hasattr(serviceProvider, _DependencyName):
            return getattr(serviceProvider, _DependencyName)

        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(_ClassToRegister.__init__).parameters.items()
                                            if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]
        
        if not _DependencyParametersFromConstructor:
            setattr(serviceProvider, _DependencyName, providerMethod(_ClassToRegister))
            return getattr(serviceProvider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(Wiring.RegisterDependency(serviceProvider, _Dependency.annotation, interfaceRegistry))

        setattr(serviceProvider, _DependencyName, providerMethod(_ClassToRegister, *_SubDependencies))
        return getattr(serviceProvider, _DependencyName)


    @staticmethod
    def ConstructUseCaseInvoker(
        serviceProvider: ServiceProvider,
        useCaseLocations: Optional[List[str]] = ["."],
        directoryExclusionPatterns: Optional[List[str]] = [],
        fileExclusionPatterns: Optional[List[str]] = []) -> UseCaseInvoker:

        _UseCaseRegistry = Wiring.ConstructUseCaseRegistry(serviceProvider, useCaseLocations, directoryExclusionPatterns, fileExclusionPatterns)

        _PipelineFactoryRegistrationName = Wiring.__GetServiceName(PipelineFactory)

        if not hasattr(serviceProvider, _PipelineFactoryRegistrationName):
            setattr(serviceProvider, _PipelineFactoryRegistrationName, providers.Singleton(PipelineFactory, pipeRegistry=_UseCaseRegistry))

        _PipelineFactory = getattr(serviceProvider, _PipelineFactoryRegistrationName)
        
        _UseCaseInvokerRegistrationName = Wiring.__GetServiceName(UseCaseInvoker)

        if not hasattr(serviceProvider, _UseCaseInvokerRegistrationName):
            setattr(serviceProvider, _UseCaseInvokerRegistrationName, providers.Factory(UseCaseInvoker, pipelineFactory=_PipelineFactory))
        
        return getattr(serviceProvider, _UseCaseInvokerRegistrationName)


    @staticmethod
    def ConstructUseCaseRegistry(
        serviceProvider: ServiceProvider,
        useCaseLocations: Optional[List[str]] = ["."],
        directoryExclusionPatterns: Optional[List[str]] = [],
        fileExclusionPatterns: Optional[List[str]] = []) -> Dict[str, List[Type[IPipe]]]:

        directoryExclusionPatterns = directoryExclusionPatterns + DIR_EXCLUSIONS
        fileExclusionPatterns = fileExclusionPatterns + FILE_EXCLUSIONS

        _UseCaseRegistry = {}

        for _Location in useCaseLocations:
            for _Root, _Directories, _Files in os.walk(_Location):
                _DirectoryNamespace = _Root.replace('/', '.')

                for _ExclusionPattern in directoryExclusionPatterns:
                    _Directories[:] = [d for d in _Directories if not re.match(_ExclusionPattern, d)]

                for _ExclusionPattern in fileExclusionPatterns:
                    _Files[:] = [f for f in _Files if not re.match(_ExclusionPattern, f)]

                _Pipes = []

                for _File in _Files:
                    _Namespace = _DirectoryNamespace + "." + _File[:-3]

                    _Class = Wiring.ImportClassByNamespace(_Namespace)

                    if issubclass(_Class, IPipe):
                        try:
                            _Pipes.append(Wiring.GetService(serviceProvider, _Class))
                        except TypeError:
                            raise InterfaceNotImplementedError(_Namespace) #TODO: I'm getting a lot of other errors reported here
                if _Pipes:
                    _UseCaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

        return _UseCaseRegistry


    @staticmethod
    def ImportClassByNamespace(namespace: str):
        _ModuleName = namespace.rsplit(".", 1)[1]
        _Module = importlib.import_module(namespace, package=None)
        _ModuleClass = getattr(_Module, _ModuleName, None)

        if _ModuleClass is None:
            raise Exception(f"""Could not find class for '{_ModuleName}'. Classes must be named the same as their module
            to be registered in the dependency container. If you do not want this module to be scanned, add it to the
            file exclusions, or be more specific with your scan locations.""")

        return _ModuleClass


    @staticmethod
    def SetPipePriority(**kwargs):
        for key, value in Wiring.__GetDefaultPipePriorities().items():
            setattr(PipePriority, key, value)

        for key, value in kwargs.items():
            setattr(PipePriority, key, value)


    @staticmethod
    def __GetDefaultPipePriorities():
        return {
            f'{IAuthenticationVerifier.__name__}': 1,
            f'{IEntityExistenceChecker.__name__}': 2,
            f'{IAuthorisationEnforcer.__name__}': 3,
            f'{IBusinessRuleValidator.__name__}': 4,
            f'{IInputPortValidator.__name__}': 5,
            f'{IInteractor.__name__}': 6
        }
