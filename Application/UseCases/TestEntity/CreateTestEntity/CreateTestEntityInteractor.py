from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Dtos.TestDto import TestDto
from Domain.Entities.TestEntity import TestEntity
import uuid
from dependency_injector.wiring import inject, Provide

class CreateTestEntityInteractor(IInteractor):

    @inject
    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        x = TestEntity(id=uuid.uuid4(), testText=inputPort._input)
        self._persistence.Add(self, tEntity=x)
        outputPort.PresentTest(TestDto(id=uuid.uuid4(), testText=inputPort._input))
        return True
