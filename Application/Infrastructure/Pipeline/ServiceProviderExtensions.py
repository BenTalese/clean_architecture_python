from abc import ABC
import importlib
import inspect
import os
import re
import sys
from Application.Infrastructure.Pipeline.ServiceProvider import ServiceProvider
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInputPort import CreateTestEntityInputPort
from Application.UseCases.TestEntity.CreateTestEntity.CreateTestEntityInteractor import CreateTestEntityInteractor
from Framework.CreateTestEntityPresenter import CreateTestEntityPresenter
from dependency_injector import providers
from typing import List, Tuple

sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

class ServiceProviderExtensions: # TODO: Rename to Wiring or something

    @staticmethod
    def GetService(serviceProvider, service: object) -> object:
        try:
            return serviceProvider.providers.get(service.__name__)()
        except Exception as e:
            print(f"Was not able to retrive '{service.__name__}' from DI container. (Original exception: {e}.)")

    # TODO: Register pipelinescanner as singleton
    # TODO: Register pipelinefactory as singleton
    @staticmethod
    def ConstructServiceProvider( # BuildClapyEngine()? Wiring.BuildEngine()?
        serviceProvider,
        usecase_scan_locations: List[str],
        scan_locations: List[str],
        directory_exclusion_list: List[str],
        file_exclusion_list: List[str]): #ConfigureServices():
        pass

    # TODO: Separate this into different methods
    # TODO: Add ability for user to specify "pls scan everything", which may take the form of "*" in the location list or an empty list
    # TODO: Currently this registers everything as a factory (need option to do singleton)
    @staticmethod
    def RegisterDependencies(
        serviceProvider: ServiceProvider,
        scanLocations: List[str],
        directoryExclusionList: List[str],
        fileExclusionList: List[str],
        interfaceRegistry: List[Tuple[type, type]]): #TODO: type hint this

        for location in scanLocations:
            for root, directories, files in os.walk(location):
                directories[:] = [d for d in directories if d not in directoryExclusionList]
                files[:] = [f for f in files if f not in fileExclusionList]
                for file in files:
                    module_name = file[:-3]
                    module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}", package=None)
                    module_class = getattr(module, module_name, None)
                    constructor_params = inspect.signature(module_class.__init__).parameters
                    subDependencies = []

                    ServiceProviderExtensions.RecursiveRegister(serviceProvider, module_name, module_class, constructor_params, interfaceRegistry)

                    """
                    for parameter_name, parameter in constructor_params.items():
                        parameter_type = parameter.annotation
                        if (parameter_type != inspect.Parameter.empty # TODO: could potentially check if DI_ specified but parameter is empty and then raise exception
                            and parameter_name.startswith("DI_")):

                            _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(parameter_type))
                            if _TypeMatch: # TODO: Completely skips over if type not matched...? Could be bad??
                                _DependencyName = _TypeMatch.group().replace('.', '')
                                ServiceProviderExtensions.RegisterDependency(serviceProvider, _DependencyName, parameter_type, interfaceRegistry, None)
                                subDependencies.append(getattr(serviceProvider, _DependencyName))

                    ServiceProviderExtensions.RegisterDependency(serviceProvider, module_name, module_class, interfaceRegistry, subDependencies)
                    """
                    # TODO: Investigate if this won't work if the class to be registered does not match file name

        v = serviceProvider.providers.get("CreateTestEntityInteractor")()
        valid_input_port = CreateTestEntityInputPort("Hello")
        output_port = CreateTestEntityPresenter()
        v.Execute(valid_input_port, output_port)
        vb = 0

    #ImplementationProvider class?
    #Could have CheckIfInterface()?
    @staticmethod
    def __TryGetConcreteImplementation():
        pass

    @staticmethod
    def RecursiveRegister(serviceProvider, name, type, const, interfaceRegistry):
        if not any(paramName.startswith("DI_") for paramName, param in const.items()):
            ServiceProviderExtensions.RegisterDependency(serviceProvider, name, type, interfaceRegistry, None)
            return getattr(serviceProvider, name)
        
        subdeps = [param for paramName, param in const.items() if paramName.startswith("DI_")]

        things = []
        for subdep in subdeps:
            things.append(ServiceProviderExtensions.RecursiveRegister(serviceProvider, subdep.name, subdep.annotation, inspect.signature(subdep.annotation.__init__).parameters, interfaceRegistry))
        
        ServiceProviderExtensions.RegisterDependency(serviceProvider, name, type, interfaceRegistry, things)


    @staticmethod
    def RegisterDependency(serviceProvider, name: str, type: type, interfaceRegistry: List[Tuple[type, type]], subDependencies: List[type]): # TODO: Confirm if correct type hints
        members = inspect.getmembers(serviceProvider)
        for member in members:
            _MemberMatch = re.search(r"'([^']*)'", str(member[1]))
            _TypeMatch = re.search(r"'([^']*)'", str(type))
            if _MemberMatch and _TypeMatch and _MemberMatch.group(1) == _TypeMatch.group(1):
                print(f"Skipped registering '{name}' of type {type} because '{member[0]}' is already registered as {member[1]}.") # TODO: Could be logged
                return
        # TODO: PROBLEM - Outside code thinks it succeeds anyways
        if hasattr(serviceProvider, name):
            print(f"Skipped registering {name} of type {type} because container already has {name} registered.")
            return

        isInterface = ABC in type.__bases__

        if isInterface and type not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
            raise LookupError(f"Interface '{type.__name__}' does not have a concrete class registered.")

        concreteClass = None
        if isInterface:
            concreteClass = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == type][0] #TODO: investigate if this requires [0] on the end of this line, might've been there before for picking first in list if there were multiple matches...may need to be prevented

        setattr(
            serviceProvider,
            name,
            providers.Factory(
                concreteClass if concreteClass is not None else type,
                *subDependencies if subDependencies is not None else ()
            )
        )

    @staticmethod
    def RegisterPipeline(): #enum thing?
        pass

    @staticmethod
    def ConfigurePipelineScanner():
        pass

    @staticmethod
    def ConfigurePipelineFactory():
        pass


"""
    @staticmethod
    def RegisterDependencyOLD(serviceProvider, name: str, type: type, interfaceRegistry: List[Tuple[type, type]], subDependencies: List[type]): # TODO: Confirm if correct type hints
        if ABC in type.__bases__:
            if type in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
                concreteClass = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == type] #TODO: investigate if this requires [0] on the end of this line
                if not hasattr(serviceProvider, name):
                    setattr(serviceProvider, name, concreteClass) # TODO: this could have sub dependencies
            else:
                raise LookupError(f"Interface '{type.__name__}' does not have a concrete class registered.")
        else:
            if not hasattr(serviceProvider, name):
                setattr(
                    serviceProvider,
                    name,
                    providers.Factory(type, *subDependencies.values()) # TODO: only do subdependencies if there are any
                )

    @staticmethod
    def RegisterDependencyOLDBUTNOTOLDOLD(serviceProvider, name: str, type: type, interfaceRegistry: List[Tuple[type, type]], subDependencies: List[type]): # TODO: Confirm if correct type hints
        isInterface = ABC in type.__bases__

        if isInterface and type not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
            raise LookupError(f"Interface '{type.__name__}' does not have a concrete class registered.")

        if isInterface:
            concreteClass = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == type] #TODO: investigate if this requires [0] on the end of this line

        if not hasattr(serviceProvider, name):
            setattr(
                serviceProvider,
                name,
                providers.Factory(
                    concreteClass if concreteClass is not None else type,
                    *subDependencies.values() if subDependencies is not None else None
                ) # TODO: only do subdependencies if there are any
            )
"""
