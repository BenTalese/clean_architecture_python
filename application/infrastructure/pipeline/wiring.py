from abc import ABC
import importlib
import inspect
import os
import re
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipeline.pipe_priority import PipePriority
from application.infrastructure.pipeline.pipeline_factory import PipelineFactory
from application.infrastructure.pipeline.service_provider import ServiceProvider
from application.infrastructure.pipeline.usecase_invoker import UseCaseInvoker
from application.infrastructure.pipes.iauthentication_verifier import IAuthenticationVerifier
from application.infrastructure.pipes.iauthorisation_enforcer import IAuthorisationEnforcer
from application.infrastructure.pipes.ibusiness_rule_validator import IBusinessRuleValidator
from application.infrastructure.pipes.ientity_existence_checker import IEntityExistenceChecker
from application.infrastructure.pipes.iinput_port_validator import IInputPortValidator
from application.infrastructure.pipes.iinteractor import IInteractor
from application.infrastructure.pipes.ipipe import IPipe
from dependency_injector import providers
from typing import Dict, List, Optional, Tuple, Type

from domain.errors.interface_not_implemented_error import InterfaceNotImplementedError


#TODO: find a place for this to live
DIR_EXCLUSIONS = [r"__pycache__"]
FILE_EXCLUSIONS = [r".*__init__\.py", r".*OutputPort\.py"]


class Wiring:

    @staticmethod
    def _get_service_name(service: Type) -> str:
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            raise Exception(f"Could not detect class name from fully qualified name of {service}.")

        return _TypeMatch.group().replace('.', '_')


    @staticmethod
    def get_service(service_provider: ServiceProvider, service: Type) -> object:
        _ServiceName = Wiring._get_service_name(service)

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

                    Wiring.register_dependency(service_provider, _Class, interface_registry)


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
    @staticmethod
    def register_dependency(
        service_provider: ServiceProvider,
        class_type: Type,
        interface_registry: List[Tuple[type, type]],
        provider_method: Optional[Type] = providers.Factory) -> object:

        _ClassToRegister = Wiring._try_get_concrete_type(class_type, interface_registry)
        _DependencyName = Wiring._get_service_name(_ClassToRegister)

        if hasattr(service_provider, _DependencyName):
            return getattr(service_provider, _DependencyName)

        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(_ClassToRegister.__init__).parameters.items()
                                                    if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]
        
        if not _DependencyParametersFromConstructor:
            setattr(service_provider, _DependencyName, provider_method(_ClassToRegister))
            return getattr(service_provider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(Wiring.register_dependency(service_provider, _Dependency.annotation, interface_registry))

        setattr(service_provider, _DependencyName, provider_method(_ClassToRegister, *_SubDependencies))
        return getattr(service_provider, _DependencyName)


    @staticmethod
    def construct_usecase_invoker(
        service_provider: ServiceProvider,
        usecase_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> UseCaseInvoker:

        _UsecaseRegistry = Wiring._construct_usecase_registry(service_provider, usecase_locations, directory_exclusion_patterns, file_exclusion_patterns)

        _PipelineFactoryRegistrationName = Wiring._get_service_name(IPipelineFactory)

        if not hasattr(service_provider, _PipelineFactoryRegistrationName):
            setattr(service_provider, _PipelineFactoryRegistrationName, providers.Singleton(PipelineFactory, usecase_registry=_UsecaseRegistry))

        _PipelineFactory = getattr(service_provider, _PipelineFactoryRegistrationName)
        
        _UsecaseInvokerRegistrationName = Wiring._get_service_name(IUseCaseInvoker)

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
                        try:
                            _Pipes.append(Wiring.get_service(service_provider, _Class))
                        except TypeError:
                            raise InterfaceNotImplementedError(_Namespace) #TODO: I'm getting a lot of other errors reported here
                if _Pipes:
                    _UsecaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

        return _UsecaseRegistry


    @staticmethod
    def _import_class_by_namespace(namespace: str):
        _ModuleName = "".join([s[0].upper() for s in namespace.rsplit(".", 1)[1].split("_")])
        #_Module = importlib.import_module(namespace, package=None)
        #_ModuleClass = getattr(_Module, _ModuleName, None)
        _ModuleClass = inspect.getmembers(importlib.import_module(namespace, package=None), inspect.isclass)[0][1]


        if _ModuleClass is None:
            raise Exception(f"""Could not find class for '{_ModuleName}'. Classes must be named the same as their module
            to be registered in the dependency container. If you do not want this module to be scanned, add it to the
            file exclusions, or be more specific with your scan locations.""")

        return _ModuleClass


    @staticmethod
    def set_pipe_priority(**kwargs):
        for key, value in Wiring._get_default_pipe_priorities().items():
            setattr(PipePriority, key, value)

        for key, value in kwargs.items():
            setattr(PipePriority, key, value)


    @staticmethod
    def _get_default_pipe_priorities():
        return {
            f'{IAuthenticationVerifier.__name__}': 1,
            f'{IEntityExistenceChecker.__name__}': 2,
            f'{IAuthorisationEnforcer.__name__}': 3,
            f'{IBusinessRuleValidator.__name__}': 4,
            f'{IInputPortValidator.__name__}': 5,
            f'{IInteractor.__name__}': 6
        }
