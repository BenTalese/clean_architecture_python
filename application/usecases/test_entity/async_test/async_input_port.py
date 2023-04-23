
from application.infrastructure.pipes.iinput_port import IInputPort


class AsyncInputPort(IInputPort):

    def __init__(self, input: int, order: int):
        self.order = order
        self.input = input
