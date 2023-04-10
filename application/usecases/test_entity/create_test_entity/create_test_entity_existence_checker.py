from typing import Callable
from application.infrastructure.pipes.ientity_existence_checker import IEntityExistenceChecker
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort


class CreateTestEntityExistenceChecker(IEntityExistenceChecker[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def execute(self, input_port: CreateTestEntityInputPort, output_port: ICreateTestEntityOutputPort) -> Callable | None:
        pass
