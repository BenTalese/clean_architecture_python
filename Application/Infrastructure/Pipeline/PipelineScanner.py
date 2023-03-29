import importlib
import inspect
import os
import sys
from abc import ABC
from typing import Dict, List, Type
from Application.Infrastructure.Pipeline.Container import Container
from Application.Infrastructure.Pipeline.ContainerExtensions import ContainerExtensions
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Application.Infrastructure.Pipes.IPipe import IPipe

from Domain.Errors.InterfaceNotImplementedError import InterfaceNotImplementedError


sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

class PipelineScanner:
    def __init__(self, container: Container, parent_use_case_folder_path: str):
        self._container = container
        self._parent_use_case_folder_path = parent_use_case_folder_path

    test2 = os.path.dirname(os.path.realpath(__file__)) #'/home/benny/Repos/clean_architecture_python/Application/Infrastructure/Pipeline' (could set globally...)

    def scan(self) -> Dict[str, List[Type[IPipe]]]:
        pipes_registry = {}
        for root, dirs, files in os.walk(self._parent_use_case_folder_path):
            if "__pycache__" in dirs:
                dirs.remove("__pycache__") #also could do for file... if file.endswith(".py")
            pipes = []
            for file in files:
                module_name = file[:-3]
                module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}", package=None)
                obj = getattr(module, module_name, None)
                if issubclass(obj, IPipe):
                    try:
                        pipe = ContainerExtensions.GetService(self._container, obj)
                        pipes.append(pipe)
                    except TypeError:
                        raise InterfaceNotImplementedError(module_name)
            if pipes:
                pipes_registry[root.replace('/', '.')] = { "pipes": pipes }
                #pipes_registry[root.split("/")[-1]] = { "pipes": pipes }
                #pipes_registry[os.path.basename(dirpath)] = {"interactor": CreateTestEntityInteractor(Persistence()), "pipes": pipes}

        return pipes_registry
