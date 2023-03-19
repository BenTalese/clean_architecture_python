class UseCaseInvoker():
    def InvokeUseCase():
        pass

    def CanInvokeUseCase(): #is this even necessary if i can stop the pipe if there's errors?
        pass

#TODO: Figure out how to stop the pipe invocation if entity does not exist
#IDEA: Could instead return None for all pipes, and IPipe can have "PipelineShouldContinue or CanInvokeNextPipe" which is checked each time, is only set for fatal error type issues