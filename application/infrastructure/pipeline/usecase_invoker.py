from asyncio import Task
import asyncio
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
        while _PipelineResult is None and len(_Pipeline) > 0:

            _Pipe = _Pipeline.pop(0)

            _PipelineResult = _Pipe.execute(input_port, output_port)

        _PipelineResult()


    async def invoke_usecase_async(self, input_port: TInputPort, output_port: TOutputPort) -> None:
        _Pipeline = self._pipeline_factory.create_pipeline(input_port)

        _PipelineResult = None
        while _PipelineResult is None and len(_Pipeline) > 0:
            _Pipe = _Pipeline.pop(0)
            _PipelineResult = await _Pipe.execute_async(input_port, output_port)

            if _PipelineResult is not None:
                await _PipelineResult
                break
