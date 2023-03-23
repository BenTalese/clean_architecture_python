import os
import sys

from Framework.Infrastructure.Persistence import Persistence
sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPortValidator import CreateTestEntityInputPortValidator
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Domain.Infrastructure.Generics import TInteractor, TOutputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter


class Pipeline:
    def __init__(self, interactor: TInteractor):
        self.interactor = interactor
        self.pipes = []

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def execute(self, input_port: IInputPort, output_port: TOutputPort):
        errors = []
        for pipe in self.pipes:
            try:
                pipe.Validate(input_port, output_port)
            except Exception as e:
                errors.append(str(e))
        
        if errors:
            output_port.PresentValidationFailure(errors)
        else:
            self.interactor.Handle(input_port, output_port)


# Create the interactor instance
interactor = CreateTestEntityInteractor(Persistence())

# Create the pipeline and add the pipes
pipeline = Pipeline(interactor)
pipeline.add_pipe(CreateTestEntityInputPortValidator())
#pipeline.add_pipe(Pipe2())
#pipeline.add_pipe(Pipe3())

# Create the input and output ports
invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()

# Execute the pipeline
pipeline.execute(valid_input_port, output_port)
pipeline.execute(invalid_input_port, output_port)