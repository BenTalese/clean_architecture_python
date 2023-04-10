from application.infrastructure.pipes.iinput_port import IInputPort

class CreateTestEntityInputPort(IInputPort):

    def __init__(self, input: str):
        self.input = input
