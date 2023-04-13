from application.infrastructure.pipeline.dependency_injection import register_service
from application.infrastructure.pipeline.service_provider import ServiceProvider
from application.infrastructure.pipeline.wiring import construct_usecase_invoker, set_pipe_priority
from application.services.ipersistence import IPersistence
from application.services.itest_service import ITestService
from application.usecases.test_entity.create_test_entity.create_test_entity_input_port import CreateTestEntityInputPort
from dependency_injector import providers
from framework.create_test_entity_presenter import CreateTestEntityPresenter
from framework.infrastructure.persistence import Persistence
from framework.infrastructure.test_infrastructure import TestInfrastructure

_ServiceProvider = ServiceProvider()

def RegisterStuff(service_provider: ServiceProvider):
    register_service(service_provider, providers.Factory, TestInfrastructure, ITestService) #TODO: important to point out to user that order of registration matters
    register_service(service_provider, providers.Factory, Persistence, IPersistence)

RegisterStuff(_ServiceProvider)

_UsecaseScanLocations = ["application/usecases"]

set_pipe_priority(IAuthorisationEnforcer=0, IAuthenticationVerifier=3)
_Invoker = construct_usecase_invoker(_ServiceProvider, _UsecaseScanLocations)

_InvalidInputPort = CreateTestEntityInputPort("test")
_ValidInputPort = CreateTestEntityInputPort("Hello")
_OutputPort = CreateTestEntityPresenter()

_Invoker.invoke_usecase(_ValidInputPort, _OutputPort)
