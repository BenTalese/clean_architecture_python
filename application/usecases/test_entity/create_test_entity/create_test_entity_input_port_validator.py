from typing import Callable
from application.infrastructure.pipes.iinput_port_validator import IInputPortValidator
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort


class CreateTestEntityInputPortValidator(IInputPortValidator[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def execute(self, input_port: CreateTestEntityInputPort, output_port: ICreateTestEntityOutputPort) -> Callable | None:
        _Failures = []

        if input_port._input != "Hello":
            _Failures.append("Text was not 'Hello'.")
            _Failures.append("Another message for testing.")
            return lambda: output_port.present_validation_failure(_Failures)
