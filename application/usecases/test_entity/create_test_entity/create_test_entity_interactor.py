from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort
from Application.Dtos.TestDto import TestDto
from Domain.Entities.TestEntity import TestEntity
import uuid

class CreateTestEntityInteractor(IInteractor):

    def __init__(self, DI_persistence: IPersistence):
        self._persistence = DI_persistence
    
    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        print("CreateTestEntityInteractor")
        x = TestEntity(id=uuid.uuid4(), testText=inputPort._input)
        self._persistence.Add(tEntity=x)
        outputPort.PresentTest(TestDto(id=uuid.uuid4(), testText=inputPort._input))
        return True
