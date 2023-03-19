import os
import importlib
import inspect

class PipelineScanner:
    def __init__(self, use_case_dir):
        self.use_case_dir = use_case_dir

    def scan(self):
        pipes_registry = {}
        for file in os.listdir(self.use_case_dir):
            if file.endswith("_use_case.py"):
                module_name = file[:-3]
                module = importlib.import_module(f"{self.use_case_dir}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, IInteractor) and obj != IInteractor:
                        pipes = [c() for _, c in inspect.getmembers(module, inspect.isclass) if
                                 issubclass(c, IInputPortValidator) and c != IInputPortValidator]
                        pipes_registry[name] = {"interactor": obj(), "pipes": pipes}

        return pipes_registry
    
class PipelineScanner:
    def __init__(self, use_case_dir):
        self.use_case_dir = use_case_dir

    def scan(self):
        pipes_registry = {}
        use_case_dir = os.path.join(self.use_case_dir, "Use Cases")
        for file in os.listdir(use_case_dir):
            if file.endswith("_use_case.py"):
                module_name = file[:-3]
                module = importlib.import_module(f"{self.use_case_dir}.Use Cases.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, IInteractor) and obj != IInteractor:
                        pipes = [c() for _, c in inspect.getmembers(module, inspect.isclass) if
                                 issubclass(c, IInputPortValidator) and c != IInputPortValidator]
                        pipes_registry[name] = {"interactor": obj(), "pipes": pipes}

        return pipes_registry

class PipelineScanner:
    def __init__(self, use_case_dir):
        self.use_case_dir = use_case_dir

    def scan(self):
        pipes_registry = {}
        for root, dirs, files in os.walk(os.path.join(self.use_case_dir, "Use Cases")):
            for file in files:
                if file.endswith("_use_case.py"):
                    module_name = file[:-3]
                    module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}")
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, IInteractor) and obj != IInteractor:
                            pipes = [c() for _, c in inspect.getmembers(module, inspect.isclass) if
                                     issubclass(c, IInputPortValidator) and c != IInputPortValidator]
                            pipes_registry[name] = {"interactor": obj(), "pipes": pipes}

        return pipes_registry





class PipeScanner:
    def __init__(self, directory: str):
        self._directory = directory

    def scan(self) -> Dict[str, List[Type[Pipe]]]:
        use_cases = {}
        for file_name in os.listdir(self._directory):
            if file_name.startswith('__'):
                continue
            path = os.path.join(self._directory, file_name)
            if os.path.isdir(path):
                use_case_name = file_name.replace(' ', '')
                use_cases[use_case_name] = self._scan_use_case(path)
        return use_cases

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