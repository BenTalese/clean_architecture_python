import os
import importlib
import inspect
from typing import Dict, List, Type
from abc import ABC

import sys
sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...


from Application.Infrastructure.Pipes.IPipe import IPipe



"""
class PipeScanner:

        for file_name in os.listdir(self._directory):
            if file_name.startswith('__'):
                continue
            path = os.path.join(self._directory, file_name)
            if os.path.isdir(path):
                use_case_name = file_name.replace(' ', '')
                use_cases[use_case_name] = self._scan_use_case(path)

    def _scan_use_case(self, path: str) -> List[Type[Pipe]]:
        pipes = []
        for file_name in os.listdir(path):
            if file_name.startswith('__'):
                continue
            if file_name.endswith('.py'):
                module_name = file_name[:-3]
                module = __import__(f'{path}.{module_name}', fromlist=[module_name])
                for member in inspect.getmembers(module):
                    if inspect.isclass(member[1]) and issubclass(member[1], Pipe) and member[1] != Pipe:
                        pipes.append(member[1])
        return pipes

module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}")
module = importlib.import_module(f"{self.use_case_dir}.Use Cases.{module_name}")
if inspect.isclass(obj) and issubclass(obj, IInteractor) and obj != IInteractor:
    pipes = [c() for _, c in inspect.getmembers(module, inspect.isclass) if
                issubclass(c, IInputPortValidator) and c != IInputPortValidator]
    pipes_registry[name] = {"interactor": obj(), "pipes": pipes}
"""    


class PipelineScanner:
    def __init__(self, parent_use_case_folder_path: str):
        self._parent_use_case_folder_path = parent_use_case_folder_path

    test2 = os.path.dirname(os.path.realpath(__file__)) #'/home/benny/Repos/clean_architecture_python/Application/Infrastructure/Pipeline' (could set globally...)

    print(dir(inspect))

    def scan(self) -> Dict[str, List[Type[IPipe]]]:
        pipes_registry = {}
        for root, dirs, files in os.walk(self._parent_use_case_folder_path):
            for file in files:
                module_name = file[:-3]
                module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    pipes = []
                    if module_name != "ICreateTestEntityOutputPort": #should be own method (not the forbidden types)
                        if issubclass(obj, IPipe): #should be own method (not the forbidden types)
                    #if (issubclass(obj, IPipe) and module_name != "ICreateTestEntityOutputPort"): #should be own method (not the forbidden types)
                            pipes.append(obj())
                    pipes_registry[name] = {"interactor": obj(), "pipes": pipes}

        print(pipes_registry)

        return pipes_registry
    
PipelineScanner("Application/UseCases").scan()