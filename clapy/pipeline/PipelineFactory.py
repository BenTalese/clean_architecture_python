from typing import List, Type
from clapy.pipes.IInputPort import IInputPort
from clapy.pipes.IPipe import IPipe

class PipelineFactory:
    def __init__(self, pipes_registry):
        self.pipes_registry = pipes_registry

    def create_pipeline(self, inputPort: IInputPort) -> List[Type[IPipe]]:
        usecase_key = inputPort.__module__.rsplit(".", 1)[0]

        if usecase_key not in self.pipes_registry:
            raise KeyError(f"Could not find '{inputPort}' in the pipeline registry.")
        
        pipes = self.pipes_registry[usecase_key]["pipes"]
        
        if pipes is None:
            raise Exception(f"Pipeline registry for '{inputPort}' contained no pipes.")
        
        if any(pipe is None for pipe in pipes):
            raise Exception(f"One of the pipes for the use case '{usecase_key}' is not configured correctly.")
        
        sorted_pipes = sorted(pipes, key=lambda pipe: pipe.Priority.value)
        return sorted_pipes



"""
    




class PipelineFactory:
    def __init__(self, use_case_package: str, pipe_package: str):
        self.use_case_package = use_case_package
        self.pipe_package = pipe_package

    def create_pipeline(self, use_case_name: str) -> List[Type[IPipe]]:
        use_case_module = importlib.import_module(
            f"{self.use_case_package}.{use_case_name}"
        )

        pipes = []

        for _, pipe_class in self.get_pipe_classes().items():
            if hasattr(use_case_module, pipe_class.__name__):
                pipes.append(pipe_class)

        return pipes

    def get_pipe_classes(self) -> dict:
        pipe_classes = {}

        for module_name in self.get_module_names(self.pipe_package):
            module = importlib.import_module(f"{self.pipe_package}.{module_name}")

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, IPipe) and obj != IPipe:
                    pipe_classes[obj.__name__] = obj

        return pipe_classes

    def get_module_names(self, package_name: str) -> List[str]:
        modules = []

        for file_name in os.listdir(package_name):
            if file_name.endswith(".py"):
                module_name = file_name[:-3]
                modules.append(module_name)

        return modules
    


"""
