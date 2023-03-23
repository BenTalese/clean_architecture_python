from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator


class CreateTestEntityInputPortValidator(IInputPortValidator[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):
    
    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        validationFailures = []

        if inputPort._input != "Hello":
            validationFailures.append("Text was not 'Hello'.")
            validationFailures.append("Another message for testing.")

        if validationFailures:
            outputPort.PresentValidationFailure(validationFailures)
            return False

        return True
