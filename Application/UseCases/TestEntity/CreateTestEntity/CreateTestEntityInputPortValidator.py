from .CreateTestEntityInputPort import CreateTestEntityInputPort
from .ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Application.Infrastructure.Pipes.IInputPortValidator import IInputPortValidator


class CreateTestEntityInputPortValidator(IInputPortValidator[CreateTestEntityInputPort, ICreateTestEntityOutputPort]):

    def Execute(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort) -> bool:
        #self._failures = []

        if inputPort._input != "Hello":
            self.m_Failures.append("Text was not 'Hello'.")
            self.m_Failures.append("Another message for testing.")
            outputPort.PresentValidationFailure(self.m_Failures)

        #if validationFailures:
            #outputPort.PresentValidationFailure(validationFailures)
            #return False
        
        #self._canInvokeNextPipe = False

        return True
