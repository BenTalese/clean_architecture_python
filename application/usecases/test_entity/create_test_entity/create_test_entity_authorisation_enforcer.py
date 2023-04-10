from typing import Callable
from Application.Infrastructure.Pipes.IAuthorisationEnforcer import IAuthorisationEnforcer
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort


class CreateTestEntityAuthorisationEnforcer(IAuthorisationEnforcer[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> Callable | None: #TODO: put this on everything
        return lambda: outputPort.PresentUnauthorised("TEST LAMBDA")
        #outputPort.PresentUnauthorised("You are unauthorised.")
        #self.m_CanInvokeNextPipe = False # TODO: I don't like having to set this
