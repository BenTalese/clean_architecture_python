import os
from typing import Dict, List, Optional
from application.infrastructure.pipeline.common import _apply_exclusion_filter, _import_class_by_namespace
from application.infrastructure.pipeline.exclusions import DIR_EXCLUSIONS, FILE_EXCLUSIONS
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iservice_provider import IServiceProvider
from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipeline.pipe_priority import PipePriority
from application.infrastructure.pipeline.pipeline_factory import PipelineFactory
from application.infrastructure.pipeline.usecase_invoker import UseCaseInvoker
from application.infrastructure.pipes.iauthentication_verifier import IAuthenticationVerifier
from application.infrastructure.pipes.iauthorisation_enforcer import IAuthorisationEnforcer
from application.infrastructure.pipes.ibusiness_rule_validator import IBusinessRuleValidator
from application.infrastructure.pipes.ientity_existence_checker import IEntityExistenceChecker
from application.infrastructure.pipes.iinput_port_validator import IInputPortValidator
from application.infrastructure.pipes.iinteractor import IInteractor
from application.infrastructure.pipes.ipipe import IPipe

# TODO: Method explanations, tidy up type hints, tidy up return types

@staticmethod
def construct_usecase_registry(
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

            if _Pipes:
                _UsecaseRegistry[_DirectoryNamespace] = { "pipes": _Pipes }

    return _UsecaseRegistry


@staticmethod
def set_pipe_priority(priorities: Dict[str, int]):
    for key, value in priorities.items():
        setattr(PipePriority, key, value)
