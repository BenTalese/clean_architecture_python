from application.infrastructure.pipeline.container import Container
from application.infrastructure.pipeline.dependency_injector_service_provider import DependencyInjectorServiceProvider
from application.infrastructure.pipeline.idependency_injector_service_provider import IDependencyInjectorServiceProvider
from application.infrastructure.pipeline.ipipeline_factory import IPipelineFactory
from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipeline.pipeline_factory import PipelineFactory
from application.infrastructure.pipeline.usecase_invoker import UseCaseInvoker
from application.infrastructure.pipeline.wiring import construct_usecase_registry, set_pipe_priority
from application.infrastructure.pipes.iauthentication_verifier import IAuthenticationVerifier
from application.infrastructure.pipes.iauthorisation_enforcer import IAuthorisationEnforcer
from application.infrastructure.pipes.ibusiness_rule_validator import IBusinessRuleValidator
from application.infrastructure.pipes.ientity_existence_checker import IEntityExistenceChecker
from application.infrastructure.pipes.iinput_port_validator import IInputPortValidator
from application.infrastructure.pipes.iinteractor import IInteractor
from application.services.ipersistence import IPersistence
from application.services.itest_service import ITestService
from application.usecases.test_entity.create_test_entity.create_test_entity_input_port import CreateTestEntityInputPort
from dependency_injector import providers
from framework.create_test_entity_presenter import CreateTestEntityPresenter
from framework.infrastructure.persistence import Persistence
from framework.infrastructure.test_infrastructure import TestInfrastructure

_ServiceProvider = DependencyInjectorServiceProvider()

def RegisterStuff(service_provider: IDependencyInjectorServiceProvider):
    service_provider.register_service(providers.Factory, TestInfrastructure, ITestService) #TODO: important to point out to user that order of registration matters
    service_provider.register_service(providers.Factory, Persistence, IPersistence)

RegisterStuff(_ServiceProvider)

_UsecaseScanLocations = ["application/usecases"]

set_pipe_priority({
        f'{IAuthenticationVerifier.__name__}': 1,
        f'{IEntityExistenceChecker.__name__}': 2,
        f'{IAuthorisationEnforcer.__name__}': 3,
        f'{IBusinessRuleValidator.__name__}': 4,
        f'{IInputPortValidator.__name__}': 5,
        f'{IInteractor.__name__}': 6
    })
_UsecaseRegistry = construct_usecase_registry(_UsecaseScanLocations)
_ServiceProvider.register_usecase_services(_UsecaseScanLocations)
_ServiceProvider.register_service(providers.Singleton, PipelineFactory, IPipelineFactory, _ServiceProvider, _UsecaseRegistry)
_ServiceProvider.register_service(providers.Factory, UseCaseInvoker, IUseCaseInvoker)
_Invoker = _ServiceProvider.get_service(IUseCaseInvoker)


_InvalidInputPort = CreateTestEntityInputPort("test")
_ValidInputPort = CreateTestEntityInputPort("Hello")
_OutputPort = CreateTestEntityPresenter()

_Invoker.invoke_usecase(_ValidInputPort, _OutputPort)
