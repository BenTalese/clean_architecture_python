
from asyncio import Task
import asyncio
from application.usecases.test_entity.async_test.iasync_output_port import IAsyncOutputPort
from domain.infrastructure.generics import TAuthorisationFailure, TValidationFailure


class AsyncPresenter(IAsyncOutputPort):

    async def present_test_async(self, text: int, order: int) -> None:
        print(f"Wow it worked, see!!  :  {text},   Order: {order}")
    
    async def present_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
        print(validation_failure)
