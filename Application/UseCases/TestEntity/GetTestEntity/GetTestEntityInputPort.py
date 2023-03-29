from Application.Infrastructure.Pipes.IInputPort import IInputPort

class GetTestEntityInputPort(IInputPort):
    def __init__(self, input: str):
        self._input = input
