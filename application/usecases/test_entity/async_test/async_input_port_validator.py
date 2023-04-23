from asyncio import Task
import asyncio
from typing import Callable
from application.infrastructure.pipes.iinput_port_validator import IInputPortValidator
from application.usecases.test_entity.async_test.async_input_port import AsyncInputPort
from application.usecases.test_entity.async_test.iasync_output_port import IAsyncOutputPort


class AsyncInputPortValidator(IInputPortValidator[AsyncInputPort, IAsyncOutputPort]):

    def execute(self, input_port: AsyncInputPort, output_port: IAsyncOutputPort) -> Callable | None:
        return print("")

    async def execute_async(self, input_port: AsyncInputPort, output_port: IAsyncOutputPort): #TODO: Should be async or not??
        _Failures = []

        print(f"Validator #{input_port.order} executing...")

        if input_port.input > 5:
            _Failures.append(f"Waiting time was too much: {input_port.input}, for call {input_port.order}")
            return output_port.present_validation_failure_async(_Failures)
