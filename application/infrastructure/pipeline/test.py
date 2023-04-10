
#sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

# TODO: Point out to users that they can put everything together their own way if they don't want to use the built-in wiring and service provider
# For this i should define what they are required to do to hook things up and get it going
# Will need to point out conventions that make this work out of the box, e.g.
#   - DI_ for parameters
#   - One class per file for DI
#   - Class name matches module name
#   - Interfaces must be registered first (idk if i like this one...)
#   - Possibly DI_S_ for singleton...not sure

# TODO: Pipes folder should be under services...I think, maybe also OutputPorts?
# TODO: Tell user they must overwrite pipe priority in use before assigning that priority to another pipe
# TODO: Also, can demonstrate how you could have a "definitions.py" file with "ROOT_DIR = os.path.dirname(os.path.abspath(__file__))" that can be passed to scan everything...or maybe they can just pass "." ... not sure yet
# TODO: Get rid of all the printing to the console...
# TODO: Add a Wiring.RegisterService method that the user can use to add a service (or not, don't recreate a DI container)

# TODO: Idea i had is this can be the Clapy-Auto version, but Clapy should be changed so it doesn't auto scan for things, and to resolve services, instead of DI'ing the pipe, use the "GetService()" method in the constructor
# IMPORTANT: Don't do a separate package, just provide building blocks + auto features



from application.infrastructure.pipeline.iusecase_invoker import IUseCaseInvoker
from application.infrastructure.pipeline.service_provider import ServiceProvider
from application.infrastructure.pipeline.wiring import Wiring
from application.services.ipersistence import IPersistence
from application.services.itest_service import ITestService
from application.usecases.test_entity.create_test_entity.create_test_entity_input_port import CreateTestEntityInputPort
from application.usecases.test_entity.create_test_entity.icreate_test_entity_output_port import ICreateTestEntityOutputPort
from framework.create_test_entity_presenter import CreateTestEntityPresenter
from framework.infrastructure.persistence import Persistence
from framework.infrastructure.test_infrastructure import TestInfrastructure


INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence),
    (ITestService, TestInfrastructure)
]

_DIScanLocations = ["application/usecases", "framework/infrastructure"]

_UsecaseScanLocations = ["application/usecases"]

_ServiceProvider = ServiceProvider()

Wiring.set_pipe_priority(IAuthorisationEnforcer=0, IAuthenticationVerifier=3)
Wiring.register_dependencies(_ServiceProvider, INTERFACE_TO_CONCRETE, _DIScanLocations)
x = Wiring.construct_usecase_invoker(_ServiceProvider, _UsecaseScanLocations)

_Invoker: IUseCaseInvoker = Wiring.get_service(_ServiceProvider, IUseCaseInvoker)

#_Invoker.m_ContinueOnFailures = True

_InvalidInputPort = CreateTestEntityInputPort("test")
_ValidInputPort = CreateTestEntityInputPort("Hello")
_OutputPort = CreateTestEntityPresenter()

_Invoker.invoke_usecase(_ValidInputPort, _OutputPort)


class TestController():

    def __init__(self, usecase_invoker: IUseCaseInvoker):
        self._usecase_invoker = usecase_invoker if usecase_invoker is not None else ValueError(f"'{usecase_invoker=}' cannot be None.")


    def create_test_entity(self, input_port: CreateTestEntityInputPort, output_port: ICreateTestEntityOutputPort):
        self._usecase_invoker.invoke_use_case(input_port, output_port)





"""
Style Guide

module:         example     example_module
class:          Example     ExampleClass
method:         example     example_method
parameter:      example     example_parameter
member:         example     example_member
private member: _example    _example_member
variable:       _Example    _ExampleVariable
constant:       EXAMPLE     EXAMPLE_CONSTANT

"""
