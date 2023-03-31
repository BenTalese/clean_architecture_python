from clapy.pipes.IInputPortValidator import IInputPortValidator
from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort


class CreateTestEntityInputPortValidator(IInputPortValidator[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        self._failures = []

        if inputPort._input != "Hello":
            self._failures.append("Text was not 'Hello'.")
            self._failures.append("Another message for testing.")

        #if validationFailures:
            #outputPort.PresentValidationFailure(validationFailures)
            #return False
        
        #self._canInvokeNextPipe = False

        return True
