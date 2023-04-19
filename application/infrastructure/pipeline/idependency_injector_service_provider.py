from abc import ABC, abstractmethod
from typing import List, Optional, Type
from application.infrastructure.pipeline.iservice_provider import IServiceProvider

from domain.infrastructure.generics import TServiceType


class IDependencyInjectorServiceProvider(IServiceProvider, ABC):

    @abstractmethod
    def register_service(
        self,
        provider_method: Type,
        concrete_type: Type[TServiceType],
        interface_type: Optional[Type[TServiceType]] = None,
        *args) -> None:
        pass

    
    @abstractmethod
    def register_usecase_services(
        self,
        usecase_scan_locations: Optional[List[str]] = ["."],
        directory_exclusion_patterns: Optional[List[str]] = [],
        file_exclusion_patterns: Optional[List[str]] = []) -> None:
        pass
