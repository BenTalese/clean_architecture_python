from application.infrastructure.pipes.iinput_port import IInputPort


class GetTestEntityInputPort(IInputPort):
    def __init__(self, input: str):
        self.input = input
