from Application.Infrastructure.Pipes.IEntityExistenceChecker import IEntityExistenceChecker
from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort


class CreateTestEntityExistenceChecker(IEntityExistenceChecker[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> None:

        self.m_CanInvokeNextPipe = True
