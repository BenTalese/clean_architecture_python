from Application.Services.IPersistence import IPersistence
from Application.Services.ITestService import ITestService
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Framework.Infrastructure.TestInfrastructure import TestInfrastructure
from Application.UseCases.TestEntity.CreateTestEntity.ICreateTestEntityOutputPort import ICreateTestEntityOutputPort
from Framework.Infrastructure.Persistence import Persistence
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter
from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.Infrastructure.Pipeline.Wiring import Wiring
from Application.Infrastructure.Pipeline.UseCaseInvoker import UseCaseInvoker
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter

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



INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence),
    (ITestService, TestInfrastructure)
]

di_scan_locations = ["Application/UseCases", "Framework/Infrastructure"]

_UseCaseScanLocations = ["Application/UseCases"]

_ServiceProvider = ServiceProvider()

Wiring.SetPipePriority(IAuthorisationEnforcer=0, IAuthenticationVerifier=3)
Wiring.RegisterDependencies(_ServiceProvider, INTERFACE_TO_CONCRETE, di_scan_locations)
Wiring.ConstructUseCaseInvoker(_ServiceProvider, _UseCaseScanLocations)

_Invoker: UseCaseInvoker = Wiring.GetService(_ServiceProvider, UseCaseInvoker)

#_Invoker.m_ContinueOnFailures = True

invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()

_Invoker.InvokeUseCase(valid_input_port, output_port)


class TestController():
    def __init__(self, useCaseInvoker: UseCaseInvoker):
        self._useCaseInvoker = useCaseInvoker

    def create_test_entity(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        self._useCaseInvoker.InvokeUseCase(inputPort, outputPort)





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
