from Application.Infrastructure.Pipes.IEntityExistenceChecker import IEntityExistenceChecker
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort


class CreateTestEntityExistenceChecker(IEntityExistenceChecker[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> None:

        self.m_CanInvokeNextPipe = True
