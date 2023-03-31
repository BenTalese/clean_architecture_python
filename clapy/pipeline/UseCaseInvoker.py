from typing import List
from Domain.Infrastructure.Generics import TInputPort, TOutputPort
from clapy.pipeline.PipelineFactory import PipelineFactory
from clapy.pipeline.PipelineScanner import PipelineScanner
from clapy.pipeline.ServiceProvider import ServiceProvider
from clapy.pipeline.ServiceProviderExtensions import ServiceProviderExtensions
from clapy.pipes.IInteractor import IInteractor
from clapy.pipes.IPipe import IPipe

class UseCaseInvoker:
    def __init__(self, serviceProvider: ServiceProvider):
        self.m_ServiceProvider = serviceProvider if serviceProvider is not None else ValueError(f"'{serviceProvider=}' cannot be None.")
        self.m_PipelineFactory: PipelineFactory = ServiceProviderExtensions.GetService(self.m_ServiceProvider, PipelineFactory) # this feels really stupid
        self.m_PipelineScanner: PipelineScanner = ServiceProviderExtensions.GetService(self.m_ServiceProvider, PipelineScanner)

    def Configure(self, useCaseScanLocations: List[str]):
        pass

    def InvokeUseCase(self, input_port: TInputPort, output_port: TOutputPort):
        pipeline = self.m_PipelineFactory.create_pipeline(input_port)
        failures: List[str] = []
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
