from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Dtos.TestDto import TestDto
from Domain.Entities.TestEntity import TestEntity
import uuid
from dependency_injector.wiring import inject, Provide

class CreateTestEntityInteractor(IInteractor):

    def __init__(self, DI_persistence: IPersistence):
        self._persistence = DI_persistence
    
    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        print("CreateTestEntityInteractor")
        x = TestEntity(id=uuid.uuid4(), testText=inputPort._input)
        self._persistence.Add(self, tEntity=x)
        outputPort.PresentTest(TestDto(id=uuid.uuid4(), testText=inputPort._input))
        return True
