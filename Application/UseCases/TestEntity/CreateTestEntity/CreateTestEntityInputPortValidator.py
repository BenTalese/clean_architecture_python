from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator


class TestInputPortValidator(IInputPortValidator[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):
    
    def Validate(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        validationFailures = []

        if inputPort._input != "Hello":
            validationFailures.append("Text was not 'Hello'.")
            validationFailures.append("Another message for testing.")

        if validationFailures:
            outputPort.PresentValidationFailures(validationFailures)
            return False

        return True