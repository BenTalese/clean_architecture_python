from abc import ABC
import importlib
import inspect
import os
import re
from application.infrastructure.pipeline.exclusions import DIR_EXCLUSIONS, FILE_EXCLUSIONS
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipeline.pipeline_factory import PipelineFactory
from application.infrastructure.pipeline.service_provider import ServiceProvider
from application.infrastructure.pipeline.usecase_invoker import UseCaseInvoker
from application.infrastructure.pipeline.wiring import Wiring
from application.infrastructure.pipes.ipipe import IPipe
from dependency_injector import providers
from typing import Dict, List, Optional, Tuple, Type



class AutoWiring:

    @staticmethod
    def get_service(service_provider: ServiceProvider, service: Type, interface_registry) -> object:
        service = AutoWiring._try_get_concrete_type(service, interface_registry)

        _ServiceName = Wiring._generate_service_name(service)

        if _Service := service_provider.providers.get(_ServiceName):
            return _Service()
        else:
            raise Exception(f"Was not able to retrieve '{service.__name__}' from DI container.")


    # TODO: Currently this registers everything as a factory (need option to do singleton), could be added to interface registry?
    # TODO: ^^^ This problem would be solved by manual service registration, so not what this is which is Clapy-Auto
    @staticmethod
    def register_dependencies(
        service_provider: ServiceProvider,
        interface_registry: List[Tuple[type, type]],
        dependency_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []):

        directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
        file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

        for _Location in dependency_scan_locations:
            for _Root, _Directories, _Files in os.walk(_Location):
                for _ExclusionPattern in directory_exclusion_patterns:
                    _Directories[:] = [_Dir for _Dir in _Directories if not re.match(_ExclusionPattern, _Dir)]

                for _ExclusionPattern in file_exclusion_patterns:
                    _Files[:] = [_File for _File in _Files if not re.match(_ExclusionPattern, _File)]

                for _File in _Files:
                    _Namespace = _Root.replace('/', '.') + "." + _File[:-3]
                    _Class = Wiring._import_class_by_namespace(_Namespace)

                    AutoWiring.register_dependency(service_provider, _Class, interface_registry)


    @staticmethod
    def _try_get_concrete_type(class_type: Type, interface_registry: List[Tuple[type, type]]) -> object:
        _IsInterface = ABC in class_type.__bases__

        if _IsInterface:
            if class_type not in [_Pairing[0] for _Pairing in interface_registry]:
                raise LookupError(f"Interface '{class_type.__name__}' does not have a concrete class registered.")

            return [_Pairing[1] for _Pairing in interface_registry if _Pairing[0] == class_type][0]

        return class_type


    # TODO: Currently parameters will always be registered as factories, also the module itself will also always be a factory
    # TODO: Something to think about, could use parameter name to determine factory or singleton, e.g. "DI_S_" is singleton, "DI_F_" is factory
    # TODO: Should this be private?
    # TODO: Figure out which methods should be public or private
    # Thought i could store provider method against the interface registry...but DI doesn't necessarily mean an interface
    @staticmethod
    def register_dependency(
        service_provider: ServiceProvider,
        class_type: Type,
        interface_registry: List[Tuple[type, type]],
        provider_method: Optional[Type] = providers.Factory) -> object:

        _ClassToRegister = AutoWiring._try_get_concrete_type(class_type, interface_registry)
        _DependencyName = Wiring._generate_service_name(_ClassToRegister)

        if hasattr(service_provider, _DependencyName):
            return getattr(service_provider, _DependencyName)

        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(_ClassToRegister.__init__).parameters.items()
                                                    if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]
        
        if not _DependencyParametersFromConstructor:
            setattr(service_provider, _DependencyName, provider_method(_ClassToRegister))
            return getattr(service_provider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(AutoWiring.register_dependency(service_provider, _Dependency.annotation, interface_registry))

        setattr(service_provider, _DependencyName, provider_method(_ClassToRegister, *_SubDependencies))
        return getattr(service_provider, _DependencyName)


    @staticmethod
    def construct_usecase_invoker(
        service_provider: ServiceProvider,
        usecase_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> UseCaseInvoker:

        _UsecaseRegistry = AutoWiring._construct_usecase_registry(service_provider, usecase_locations, directory_exclusion_patterns, file_exclusion_patterns)

        _PipelineFactoryRegistrationName = Wiring._generate_service_name(IPipelineFactory)

        if not hasattr(service_provider, _PipelineFactoryRegistrationName):
            setattr(service_provider, _PipelineFactoryRegistrationName, providers.Singleton(PipelineFactory, service_provider=service_provider, usecase_registry=_UsecaseRegistry))

        _PipelineFactory = getattr(service_provider, _PipelineFactoryRegistrationName)
        
        _UsecaseInvokerRegistrationName = Wiring._generate_service_name(IUseCaseInvoker)

        if not hasattr(service_provider, _UsecaseInvokerRegistrationName):
            setattr(service_provider, _UsecaseInvokerRegistrationName, providers.Factory(UseCaseInvoker, pipeline_factory=_PipelineFactory))
        
        return getattr(service_provider, _UsecaseInvokerRegistrationName)


    @staticmethod
    def _construct_usecase_registry(
        service_provider: ServiceProvider,
        usecase_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> Dict[str, List[Type[IPipe]]]:

        directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
        file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

        _UsecaseRegistry = {}

        for _Location in usecase_locations:
            for _Root, _Directories, _Files in os.walk(_Location):
                _DirectoryNamespace = _Root.replace('/', '.')

                for _ExclusionPattern in directory_exclusion_patterns:
                    _Directories[:] = [_Dir for _Dir in _Directories if not re.match(_ExclusionPattern, _Dir)]

                for _ExclusionPattern in file_exclusion_patterns:
                    _Files[:] = [_File for _File in _Files if not re.match(_ExclusionPattern, _File)]

                _Pipes = []

                for _File in _Files:
                    _Namespace = _DirectoryNamespace + "." + _File[:-3]

                    _Class = Wiring._import_class_by_namespace(_Namespace)

                    if issubclass(_Class, IPipe):
                        _Pipes.append(AutoWiring.get_service(service_provider, _Class))
                        
                if _Pipes:
                    _UsecaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

        return _UsecaseRegistry
