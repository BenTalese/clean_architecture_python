from typing import Callable
from application.dtos.test_dto import TestDto
from application.infrastructure.pipes.iinteractor import IInteractor
from application.services.ipersistence import IPersistence
from domain.entities.test_entity import TestEntity
from .create_test_entity_input_port import CreateTestEntityInputPort
from .icreate_test_entity_output_port import ICreateTestEntityOutputPort
import uuid

class CreateTestEntityInteractor(IInteractor):

    def __init__(self, DI_persistence: IPersistence):
        self._persistence = DI_persistence
    
    def execute(self, input_port: CreateTestEntityInputPort, output_port: ICreateTestEntityOutputPort) -> Callable | None:
        x = TestEntity(id=uuid.uuid4(), testText=input_port.input)
        self._persistence.add(entity=x)
        output_port.present_test(TestDto(id=uuid.uuid4(), testText=input_port.input))
        return True
