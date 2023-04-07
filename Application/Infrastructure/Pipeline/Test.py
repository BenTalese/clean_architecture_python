import os
import sys
from Application.Services.IPersistence import IPersistence
from Application.Services.ITestService import ITestService
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

# TODO: Pipes folder should be under services...I think, maybe also OutputPorts?
# TODO: Tell user they must overwrite pipe priority in use before assigning that priority to another pipe
# TODO: Also, can demonstrate how you could have a "definitions.py" file with "ROOT_DIR = os.path.dirname(os.path.abspath(__file__))" that can be passed to scan everything...or maybe they can just pass "." ... not sure yet
# TODO: Get rid of all the printing to the console...


INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence),
    (ITestService, TestInfrastructure)
]

di_scan_locations = ["Application/UseCases", "Framework/Infrastructure"]

_UseCaseScanLocations = ["Application/UseCases"]

_ServiceProvider = ServiceProvider()

Wiring.SetPipePriority(IAuthorisationEnforcer=0, IAuthenticationVerifier=3)
Wiring.RegisterDependencies(_ServiceProvider, INTERFACE_TO_CONCRETE, di_scan_locations)
_UseCaseRegistry = Wiring.ConstructUseCaseRegistry(_ServiceProvider, _UseCaseScanLocations)
Wiring.RegisterPipeline(_ServiceProvider, _UseCaseRegistry)
_Invoker: UseCaseInvoker = Wiring.GetService(_ServiceProvider, UseCaseInvoker)


# Create the input and output ports
invalid_input_port = CreateTestEntityInputPort("test")
valid_input_port = CreateTestEntityInputPort("Hello")
output_port = CreateTestEntityPresenter()

_Invoker.InvokeUseCase(invalid_input_port, output_port)


class TestController():
    def __init__(self, useCaseInvoker: UseCaseInvoker):
        self._useCaseInvoker = useCaseInvoker

    def CreateTestEntity(self, inputPort: CreateTestEntityInputPort, outputPort: ICreateTestEntityOutputPort):
        self._useCaseInvoker.InvokeUseCase(inputPort, outputPort)





"""
Style Guide

class: ExampleClass
method: ExampleMethod
parameter: exampleParameter
instance member: m_ExampleMember
local variable: _ExampleVariable
constant: EXAMPLE_CONSTANT
static member: s_ExampleMember

class: ExampleClass
method: example_method
parameter: example_parameter
instance member: _exampleMember
local variable: _ExampleVariable
constant: EXAMPLE_CONSTANT
static member: s_ExampleMember

"""
