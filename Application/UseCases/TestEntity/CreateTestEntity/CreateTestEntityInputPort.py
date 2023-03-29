from Application.Infrastructure.Pipes.IInputPort import IInputPort
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort

class CreateTestEntityInputPort(ICreateTestEntityOutputPort, IInputPort):
    def __init__(self, input: str):
        self._input = input
