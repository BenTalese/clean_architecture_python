from typing import List
from Application.Infrastructure.Pipeline.ServiceProviderExtensions import ServiceProviderExtensions
from dependency_injector import containers

class ServiceProvider(containers.DeclarativeContainer):
    def __init__(
            self,
            usecase_scan_locations: List[str],
            scan_locations: List[str],
            directory_exclusion_list: List[str],
            file_exclusion_list: List[str]):
        ServiceProviderExtensions.ConfigureServices(self, usecase_scan_locations, scan_locations, directory_exclusion_list, file_exclusion_list)


"""

        serviceProvider: ServiceProvider,
        usecase_scan_locations: List[str],
        scan_locations: List[str],
        directory_exclusion_list: List[str],
        file_exclusion_list: List[str]):
"""
