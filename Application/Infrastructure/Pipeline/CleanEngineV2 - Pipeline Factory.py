import os
import sys

from typing import List
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator

from Framework.Infrastructure.Persistence import Persistence
sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPortValidator import CreateTestEntityInputPortValidator
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Domain.Infrastructure.Generics import TInteractor, TOutputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter



class Pipeline:
    def __init__(self, interactor: TInteractor, pipes: List[IInputPortValidator]):
        self.interactor = interactor
        self.pipes = pipes

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


class PipelineFactory:
    def __init__(self, pipes_registry):
        self.pipes_registry = pipes_registry

    def create_pipeline(self, use_case_name):
        #pipes = [self.pipes_registry[p] for p in self.pipes_registry if p in use_case_name]
        pipes = self.pipes_registry[use_case_name]["pipes"]
        interactor = self.pipes_registry[use_case_name]["interactor"]
        return Pipeline(interactor, pipes)


pipes_registry = {
    "UseCase1": {
        "interactor": CreateTestEntityInteractor(Persistence()),
        "pipes": [CreateTestEntityInputPortValidator()]
    }
}

# Create the pipeline factory with the pipes registry
factory = PipelineFactory(pipes_registry)

# Create the input and output ports
invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()

# Create and execute the pipeline for UseCase1
pipeline = factory.create_pipeline("UseCase1")
pipeline.execute(valid_input_port, output_port)

# Create and execute the pipeline for UseCase2
#pipeline = factory.create_pipeline("UseCase2")
#pipeline.execute(input_port, output_port)