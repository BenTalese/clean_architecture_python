from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from clapy.pipes.IInputPort import IInputPort

class CreateTestEntityInputPort(IInputPort):
    def __init__(self, input: str):
        self._input = input
