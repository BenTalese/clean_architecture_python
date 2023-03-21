
"""

class PipelineFactory:
    def __init__(self, pipes_registry):
        self.pipes_registry = pipes_registry

    def create_pipeline(self, use_case_name):
        pipes = [self.pipes_registry[p] for p in self.pipes_registry if p in use_case_name]
        interactor = self.pipes_registry[use_case_name]["interactor"]
        return Pipeline(interactor, pipes)
    
class PipelineFactory:
    def __init__(self, scanner):
        self.scanner = scanner

    def create_pipeline(self, use_case_name):
        pipes_registry = self.scanner.scan()
        if use_case_name not in pipes_registry:
            raise ValueError(f"No pipeline found for use case {use_case_name}")
        pipes = pipes_registry[use_case_name]["pipes"]
        interactor = pipes_registry[use_case_name]["interactor"]
        return Pipeline(pipes, interactor)



class PipelineFactory:
    def __init__(self, pipe_scanner: PipeScanner):
        self.pipe_scanner = pipe_scanner

    def create_pipeline(self, use_case_name: str) -> Pipeline:
        pipes = self.pipe_scanner.scan().get(use_case_name, [])
        return Pipeline(pipes)
    







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