
from asyncio import Task
import asyncio
from typing import Callable, Coroutine
from application.infrastructure.pipes.iinteractor import IInteractor
from application.usecases.test_entity.async_test.async_input_port import AsyncInputPort
from application.usecases.test_entity.async_test.iasync_output_port import IAsyncOutputPort
from domain.infrastructure.generics import TInputPort, TOutputPort


class AsyncInteractor(IInteractor):

    async def execute_async(self, input_port: AsyncInputPort, output_port: IAsyncOutputPort) -> Coroutine | None:
        print(f"Interactor #{input_port.order} executing...")
        await asyncio.sleep(input_port.input)
        return output_port.present_test_async(input_port.input, input_port.order)
