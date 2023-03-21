from typing import Type, List

"""





class Pipeline:
    def __init__(self, interactor: IInteractor, pipes: List[IInputPortValidator]):
        self.interactor = interactor
        self.pipes = pipes

    def execute(self, input_port: IInputPort, output_port: IOutputPort):
        errors = []
        for pipe in self.pipes:
            try:
                pipe.Validate(input_port, output_port)
            except Exception as e:
                errors.append(str(e))

        if errors:
            output_port.PresentValidationFailures(errors)
        else:
            self.interactor.Handle(input_port, output_port)


class Pipeline:
    def __init__(self, pipes: List[Type[IPipe]]):
        self.pipes = [pipe() for pipe in pipes]

    def execute(self, data):
        for pipe in self.pipes:
            data = pipe.execute(data)
        return data
    


class Pipeline:
    def __init__(self, pipes: List[object], interactor: IInteractor):
        self.pipes = pipes
        self.interactor = interactor

    def execute(self, input_data: TInputPort):
        # create output port
        output_port = TestOutputPort()

        # call pipes in order
        for pipe in self.pipes:
            pipe.process(input_data, output_port)

        # call interactor
        self.interactor.Handle(input_data, output_port)

        



class UseCaseInvoker:
    def __init__(self, pipe_classes: List[Type[IPipe]]):
        self.pipe_classes = sorted(pipe_classes, key=lambda pipe_cls: pipe_cls.order)

    def invoke(self, input_port: TInputPort, output_port: TOutputPort):
        failures = []
        for pipe_cls in self.pipe_classes:
            pipe = pipe_cls()
            if isinstance(pipe, ValidationPipe):
                validation_failures = pipe.validate(input_port, output_port)
                if validation_failures:
                    failures += validation_failures
            elif isinstance(pipe, EntityExistenceCheckPipe):
                entity_exists = pipe.check_entity_existence(input_port, output_port)
                if not entity_exists:
                    failures.append("Entity does not exist.")
                    break
            elif isinstance(pipe, InteractorPipe):
                pipe.handle(input_port, output_port)


"""