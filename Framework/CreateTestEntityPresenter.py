from typing import List

from Application.Dtos.TestDto import TestDto
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Domain.Infrastructure.Generics import TAuthorisationFailure, TValidationFailure
from Framework.BasePresenter import BasePresenter


class CreateTestEntityPresenter(BasePresenter, ICreateTestEntityOutputPort):

    def PresentTest(self, dto: TestDto) -> None:
        print("Wow it worked, see!!  :  " + dto._testText)
    
    def PresentValidationFailure(self, validationFailure: TValidationFailure) -> bool:
        print(validationFailure)

    def PresentFailures(self, validationFailures):
        print(validationFailures)

    def PresentUnauthorised(self, authorisationFailure: TAuthorisationFailure) -> None:
        print(authorisationFailure)

    #def PresentValidationFailures(self, failures: List[str]) -> None:
    #    print("Oh no, something went wrongsies:" + ', '.join(failures))
