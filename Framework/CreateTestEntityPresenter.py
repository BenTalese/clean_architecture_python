from typing import List

from Application.Dtos.TestDto import TestDto
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Domain.Infrastructure.Generics import TValidationFailure
from Framework.BasePresenter import BasePresenter


class CreateTestEntityPresenter(BasePresenter, ICreateTestEntityOutputPort):

    def PresentTest(self, dto: TestDto) -> None:
        print("Wow it worked, see!!  :  " + dto._testText)
    
    def PresentValidationFailure(self, validationFailure: TValidationFailure) -> bool:
        super().PresentValidationFailure(validationFailure)

    #def PresentValidationFailures(self, failures: List[str]) -> None:
    #    print("Oh no, something went wrongsies:" + ', '.join(failures))
