import os
from typing import Dict, List, Optional
from application.infrastructure.pipeline.common import _apply_exclusion_filter, _import_class_by_namespace
from application.infrastructure.pipeline.dependency_injection import get_service, register_service
from application.infrastructure.pipeline.exclusions import DIR_EXCLUSIONS, FILE_EXCLUSIONS
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

# TODO: Method explanations, tidy up type hints, tidy up return types

@staticmethod
def construct_usecase_invoker(
    service_provider: ServiceProvider,
    usecase_locations: Optional[List[str]] = ["."],
    directory_exclusion_patterns: Optional[List[str]] = [],
    file_exclusion_patterns: Optional[List[str]] = []) -> IUseCaseInvoker:
    
    _UsecaseRegistry = construct_usecase_registry(service_provider, usecase_locations, directory_exclusion_patterns, file_exclusion_patterns)

    register_service(service_provider, providers.Singleton, PipelineFactory, IPipelineFactory, service_provider, _UsecaseRegistry)

    _PipelineFactory = get_service(service_provider, IPipelineFactory)

    register_service(service_provider, providers.Factory, UseCaseInvoker, IUseCaseInvoker, _PipelineFactory)

    return get_service(service_provider, IUseCaseInvoker)


#TODO: this is still doing two things... (create registry, also register pipes in DI container) maybe not a bad thing? idk
@staticmethod
def construct_usecase_registry(
    service_provider: ServiceProvider,
    usecase_locations: Optional[List[str]] = ["."],
    directory_exclusion_patterns: Optional[List[str]] = [],
    file_exclusion_patterns: Optional[List[str]] = []) -> Dict[str, List[str]]:

    directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
    file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

    _UsecaseRegistry = {}

    for _Location in usecase_locations:
        for _Root, _Directories, _Files in os.walk(_Location):

            _apply_exclusion_filter(_Directories, directory_exclusion_patterns)
            _apply_exclusion_filter(_Files, file_exclusion_patterns)

            _DirectoryNamespace = _Root.replace('/', '.')
            _Pipes = []

            for _File in _Files:
                _Namespace = _DirectoryNamespace + "." + _File[:-3]
                _Class = _import_class_by_namespace(_Namespace)

                if issubclass(_Class, IPipe):
                    _Pipes.append(_Namespace)
                    register_service(service_provider, providers.Factory, _Class)

            if _Pipes:
                _UsecaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

    return _UsecaseRegistry


@staticmethod
def set_pipe_priority(**kwargs):
    for key, value in _get_default_pipe_priorities().items():
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
