from typing import List

from Application.Dtos.TestDto import TestDto
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort


class CreateTestEntityPresenter(ICreateTestEntityOutputPort):
    def PresentTest(self, dto: TestDto) -> None:
        print("Wow it worked, see!!  :  " + dto._testText)
    
    def PresentValidationFailures(self, failures: List[str]) -> None:
        print("Oh no, something went wrongsies:" + ', '.join(failures))
