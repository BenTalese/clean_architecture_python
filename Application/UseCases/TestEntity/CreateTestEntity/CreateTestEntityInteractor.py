from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Services.IPersistence import IPersistence
from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Dtos.TestDto import TestDto
from Domain.Entities.TestEntity import TestEntity

class CreateTestEntityInteractor(IInteractor):

    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def Handle(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        self._persistence.Add(TestEntity(testText=inputPort._input))
        outputPort.PresentTest(TestDto(testText=inputPort._input))
