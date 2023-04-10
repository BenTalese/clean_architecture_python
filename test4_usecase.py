from abc import ABCMeta, abstractmethod
from typing import TypeVar

TInputPort = TypeVar("TInputPort")
TInteractor = TypeVar("TInteractor")
TOutputPort = TypeVar("TOutputPort")



class IPersistence(metaclass=ABCMeta):
    @abstractmethod
    def Add(self, val: int) -> None:
        pass

    def SaveChanges(self) -> None:
        pass

class Persistence(IPersistence):
    def Add(self, val: int) -> None:
        print("Added: " + str(val))
    
    def SaveChanges(self) -> None:
        print("Changes saved")

# Use case parts
class IInputPort(metaclass=ABCMeta):
    pass

class InputPort(IInputPort):
    def __init__(self, input: int):
        self._input = input

class IInputPortValidator(metaclass=ABCMeta):

    def Validate(self, inputPort: TInputPort):
        if(inputPort._input > 5):
            raise Exception("Error: Input was greater than five!")

class InputPortValidator(IInputPortValidator):
    def Validate(self, inputPort: InputPort):
        if(inputPort._input > 5):
            raise Exception("Error: Input was greater than five!")

class IOutputPort(metaclass=ABCMeta):
    @abstractmethod
    def PresentSuccess(message: str) -> None:
        pass

class IInteractor(metaclass=ABCMeta):
    @abstractmethod
    def Handle(self, inputPort: IInputPort, outputPort: IOutputPort):
        pass

class Interactor(IInteractor):
    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def Handle(self, inputPort: InputPort, outputPort: IOutputPort):
        self._persistence.Add(inputPort._input)
        outputPort.PresentSuccess("Hey, it worked!")

class Presenter(IOutputPort):
    def PresentSuccess(self, message: str) -> None:
        print(message)

class UseCaseInvoker():
    def InvokeUseCase(
            self,
            inputPort: IInputPort,
            inputPortValidator: IInputPortValidator,
            interactor: IInteractor,
            outputPort: IOutputPort
    ):
        interactor.Handle(inputPort, outputPort)

invoker = UseCaseInvoker()

invoker.InvokeUseCase(InputPort(2), Interactor(Persistence()), Presenter())