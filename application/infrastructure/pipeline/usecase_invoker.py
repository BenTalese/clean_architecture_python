
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipes.iinteractor import IInteractor
from domain.infrastructure.generics import TInputPort, TOutputPort


class UseCaseInvoker(IUseCaseInvoker):

    def __init__(self, pipeline_factory: IPipelineFactory):
        self._pipeline_factory = pipeline_factory if pipeline_factory is not None else ValueError(f"'{pipeline_factory=}' cannot be None.")


    def can_invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        _Pipeline = self._pipeline_factory.create_pipeline(input_port)

        _PipelineResult = None
        while _PipelineResult is None:

            _Pipe = _Pipeline.pop(0)

            if not isinstance(_Pipe, IInteractor):
                _PipelineResult = _Pipe.execute(input_port, output_port)

                if _PipelineResult is not None:
                    return False

            else:
                return True


    def invoke_usecase(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        _Pipeline = self._pipeline_factory.create_pipeline(input_port)

        _PipelineResult = None
        while _PipelineResult is None:

            _Pipe = _Pipeline.pop(0)

            if not isinstance(_Pipe, IInteractor):
                _PipelineResult = _Pipe.execute(input_port, output_port)

                if _PipelineResult is not None:
                    _PipelineResult()

            else:
                _Pipe.execute(input_port, output_port)()

        

    """
    def InvokeUseCaseTest(self, inputPort: TInputPort, outputPort: TOutputPort):
        _Pipeline = self.m_PipelineFactory.create_pipeline(inputPort)
        _PipelineShouldContinue = True

        _PipeResults = []
        while _PipelineShouldContinue:
            _Pipe = _Pipeline.pop(0)

            if not isinstance(_Pipe, IInteractor):
                _PipeResults.append(_Pipe.Execute(inputPort, outputPort)()) # This would require each pipe to return a lambda with their result and not call the output port
                _PipelineShouldContinue = _Pipe.CanInvokeNextPipe # Stops on fatal errors, e.g. entity does not exist

            elif not _PipeResults:
                _Pipe.Execute(inputPort, outputPort)

            # this would require all output ports to have this method on them...
            # could be handled by a parent IOutputPort interface...
            # but this is crap because it forces every presenter/framework to implement this method then
            else:
                outputPort.PresentFailures(_PipeResults)



        for _Pipe in _Pipeline:
            _Pipe: IPipe
            if _PipelineShouldContinue:
                if not isinstance(_Pipe, IInteractor):
                    x = _Pipe.Execute(inputPort, outputPort)
                    _PipelineShouldContinue = _Pipe.CanInvokeNextPipe # TODO: maybe swap to return this from the pipe itself...?
                    if x is not None:
                        return x()
                elif not any(p.m_Failures for p in _Pipeline):
                    _Pipe.Execute(inputPort, outputPort)



    # TODO: WIP
    def InvokeUseCaseAndPresentAllFailures(self, input_port: TInputPort, output_port: TOutputPort):
        pipeline = self.m_PipelineFactory.create_pipeline(input_port)
        failures = []
        pipeline_should_continue = True

        for pipe in pipeline:
            pipe: IPipe
            if pipeline_should_continue and (self.m_ShouldContinueOnFailures or not failures):
                if not isinstance(pipe, IInteractor):
                    pipe.Execute(input_port, output_port)
                    pipeline_should_continue = pipe.CanInvokeNextPipe #TODO: Currently if a pipe has failures the invoker will continue to run the other pipes, this could result in multiple output port method calls and how does an API present this?
                    if hasattr(pipe, "_failures") and pipe._failures:
                        failures.append(pipe._failures)
                elif not failures: #This assumes there is _failures as an attribute
                    pipe.Execute(input_port, output_port)

        #if failures and hasattr(output_port, "PresentFailures"):
        if failures and self.m_ShouldPresentAllFailures: # This will error if the output port doesn't have PresentFailures...which affects ALL use cases invoked by this invoker
            output_port.PresentFailures(failures) # TODO: Not sure I like this...it should either be "All output ports have a PresentFailures method" or "It's the responsibility of the pipe to present failures"
    """
