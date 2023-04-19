import inspect
import os
import re
from typing import List, Optional, Type
from application.infrastructure.pipeline.common import _import_class_by_namespace
from application.infrastructure.pipeline.exclusions import DIR_EXCLUSIONS, FILE_EXCLUSIONS
from application.infrastructure.pipeline.idependency_injector_service_provider import IDependencyInjectorServiceProvider
from application.infrastructure.pipes.ipipe import IPipe
from dependency_injector import containers
from domain.infrastructure.generics import TServiceType
from dependency_injector import providers

class DependencyInjectorServiceProvider(IDependencyInjectorServiceProvider):

    def __init__(self, container: containers.DeclarativeContainer):
        self._container = container


    def get_service(self, service: Type[TServiceType]) -> TServiceType:
        _ServiceName = self._generate_service_name(service)

        if _Service := self._container.providers.get(_ServiceName):
            return _Service()
        else:
            raise LookupError(f"Was not able to retrieve '{service.__name__}' from DI container.")


    def register_service(self, provider_method: Type, concrete_type: Type[TServiceType], interface_type: Optional[Type[TServiceType]] = None, *args) -> None:
        _DependencyName = self._generate_service_name(interface_type if interface_type is not None else concrete_type)

        if hasattr(self._container, _DependencyName):
            return

        _ConstructorDependencies = [_Param for _Param in inspect.signature(concrete_type.__init__).parameters.values()
                                        if _Param.annotation != inspect.Parameter.empty
                                        and self._has_service(_Param.annotation)]

        if not _ConstructorDependencies:
            setattr(self._container, _DependencyName, provider_method(concrete_type, *args))
        else:
            _SubDependencies = []
            for _Dependency in _ConstructorDependencies:
                _SubDependencyName = self._generate_service_name(_Dependency.annotation)
                _SubDependencies.append(getattr(self._container, _SubDependencyName))

            setattr(self._container, _DependencyName, provider_method(concrete_type, *_SubDependencies, *args))


    def register_usecase_services(
        self,
        usecase_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> None:

        directory_exclusion_patterns = directory_exclusion_patterns + DIR_EXCLUSIONS
        file_exclusion_patterns = file_exclusion_patterns + FILE_EXCLUSIONS

        for _Location in usecase_scan_locations:
            for _Root, _Directories, _Files in os.walk(_Location):
                for _ExclusionPattern in directory_exclusion_patterns:
                    _Directories[:] = [_Dir for _Dir in _Directories if not re.match(_ExclusionPattern, _Dir)]

                for _ExclusionPattern in file_exclusion_patterns:
                    _Files[:] = [_File for _File in _Files if not re.match(_ExclusionPattern, _File)]

                for _File in _Files:
                    _Namespace = _Root.replace('/', '.') + "." + _File[:-3]
                    _Class = _import_class_by_namespace(_Namespace)

                    if issubclass(_Class, IPipe):
                        self.register_service(providers.Factory, _Class)


    def _generate_service_name(self, service: Type) -> str:
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(service))

        if not _TypeMatch:
            raise Exception(f"Could not detect class name from fully qualified name of {service}.")

        return _TypeMatch.group().replace('.', '_')

    def _has_service(self, service: Type[TServiceType]) -> str:
        #return hasattr(self._container, self._generate_service_name(service))
        try:
            return hasattr(self._container, self._generate_service_name(service))
        except:
            pass
        #return any(issubclass(attr, service) for attr in vars(self._container).values())
