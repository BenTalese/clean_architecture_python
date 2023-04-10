from application.dtos.test_dto import TestDto
from application.usecases.test_entity.create_test_entity.icreate_test_entity_output_port import ICreateTestEntityOutputPort
from domain.infrastructure.generics import TAuthorisationFailure, TValidationFailure
from framework.base_presenter import BasePresenter


class CreateTestEntityPresenter(BasePresenter, ICreateTestEntityOutputPort):

    def present_test(self, dto: TestDto) -> None:
        print("Wow it worked, see!!  :  " + dto.test_text)
    
    def present_validation_failure(self, validation_failure: TValidationFailure) -> bool:
        print(validation_failure)

    def present_unauthorised(self, authorisation_failure: TAuthorisationFailure) -> None:
        print(authorisation_failure)

    #def PresentValidationFailures(self, failures: List[str]) -> None:
    #    print("Oh no, something went wrongsies:" + ', '.join(failures))
