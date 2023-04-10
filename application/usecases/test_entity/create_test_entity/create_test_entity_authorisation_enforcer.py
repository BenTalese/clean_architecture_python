from typing import Callable

from application.infrastructure.pipes.iauthorisation_enforcer import IAuthorisationEnforcer
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort


class CreateTestEntityAuthorisationEnforcer(IAuthorisationEnforcer[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def execute(self, input_port: CreateTestEntityInputPort, output_port: ICreateTestEntityOutputPort) -> Callable | None:
        pass
        #return lambda: output_port.present_unauthorised("TEST LAMBDA")
