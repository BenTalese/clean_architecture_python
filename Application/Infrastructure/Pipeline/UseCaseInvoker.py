from typing import List
from Application.Infrastructure.Pipeline.PipelineFactory import PipelineFactory
from Application.Infrastructure.Pipes.IInteractor import IInteractor
from Application.Infrastructure.Pipes.IPipe import IPipe
from Domain.Infrastructure.Generics import TInputPort, TOutputPort

class UseCaseInvoker:
    def __init__(self, pipelineFactory: PipelineFactory):
        self.m_PipelineFactory = pipelineFactory if pipelineFactory is not None else ValueError(f"'{pipelineFactory=}' cannot be None.")

    def InvokeUseCase(self, input_port: TInputPort, output_port: TOutputPort):
        pipeline = self.m_PipelineFactory.create_pipeline(input_port)
        failures: List[str] = None
        pipeline_should_continue = True
        for pipe in pipeline:
            pipe: IPipe
            if pipeline_should_continue:
                if not isinstance(pipe, IInteractor):
                    pipe.Execute(input_port, output_port)
                    pipeline_should_continue = pipe.CanInvokeNextPipe
                    if hasattr(pipe, "_failures") and pipe._failures:
                        failures.append(pipe._failures)
                elif not failures:
                    pipe.Execute(input_port, output_port)

        if failures:
            output_port.PresentValidationFailure(failures)

    def CanInvokeUseCase(self, input_port: TInputPort, output_port: TOutputPort) -> bool:
        pipeline = self._pipeline_factory.create_pipeline(input_port)
        failures = []
        pipeline_should_continue = True
        for pipe in pipeline:
            if pipeline_should_continue and not isinstance(pipe, IInteractor):
                pipeline_should_continue = pipe.Execute(input_port, output_port)
                if hasattr(pipe, "_failures") and pipe._failures:
                    failures.append(pipe._failures)

        if failures:
            return False
        else:
            return True
