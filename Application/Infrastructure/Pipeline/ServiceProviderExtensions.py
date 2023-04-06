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
from typing import List, Tuple, Type

sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

class ServiceProviderExtensions: # TODO: Rename to Wiring or something

    @staticmethod
    def GetService(serviceProvider, service: object) -> object:
        x = re.search(r"(?<=')[^']+(?=')", str(service)).group().replace('.', '_') #TODO: duplicated code, also don't use 'x'
        if _Service := serviceProvider.providers.get(x):
            return _Service()
        else:
            raise Exception(f"Was not able to retrieve '{service.__name__}' from DI container.")

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

        for _Location in scanLocations:
            for _Root, _Directories, _Files in os.walk(_Location):
                _Directories[:] = [d for d in _Directories if d not in directoryExclusionList]
                _Files[:] = [f for f in _Files if f not in fileExclusionList]
                for _File in _Files:
                    _ModuleName = _File[:-3]
                    _Module = importlib.import_module(f"{_Root.replace('/', '.')}.{_ModuleName}", package=None)
                    _ModuleClass = getattr(_Module, _ModuleName, None)

                    if _ModuleClass is None:
                        raise Exception(f"""Could not find class for '{_ModuleName}'. Classes must be named the same as their module to be registered 
                        in the dependency container. If you do not want this module to be scanned, add it to the file exclusions.""")

                    ServiceProviderExtensions.RegisterDependency(serviceProvider, _ModuleClass, interfaceRegistry)

        # TODO: Delete this test code
        v = ServiceProviderExtensions.GetService(serviceProvider, CreateTestEntityInteractor)
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
    def RegisterDependency(serviceProvider: ServiceProvider, classType: Type, interfaceRegistry: List[Tuple[type, type]]): #TODO: type is actually class though, might need to call it 'cls', 'classObj' or 'classInstance'
        
        # Check if registering interface, if so swap to concrete implementation
        _IsInterface = ABC in classType.__bases__

        if _IsInterface:
            if classType not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
                raise LookupError(f"Interface '{classType.__name__}' does not have a concrete class registered.")

            classType = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == classType][0]

        # Get proper name to register by (e.g. Application_UseCases_CreateTestEntity_CreateTestEntityInteractor_CreateTestEntityInteractor)
        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(classType))

        if not _TypeMatch: #TODO: investigate if this is even necessary...how would there never be a match?
            raise Exception(f"Could not detect class from fully qualified name of {classType}.")

        _DependencyName = _TypeMatch.group().replace('.', '_')

        # Check if already registered, if so return that one instead
        for member in inspect.getmembers(serviceProvider):
            _MemberMatch = re.search(r"'([^']*)'", str(member[1]))
            _TypeMatch = re.search(r"'([^']*)'", str(classType))
            if _MemberMatch and _TypeMatch and _MemberMatch.group(1) == _TypeMatch.group(1):
                print(f"Skipped registering class of type {classType} because '{member[1]}' is already registered to {member[0]}.") # TODO: Could be logged
                return getattr(serviceProvider, _DependencyName)

        # TODO: figure out if above and below checks can be merged, feels redundant

        # Check if attribute taken, if so return that one instead of registering a new one
        if hasattr(serviceProvider, _DependencyName):
            print(f"Skipped registering {_DependencyName} of type {classType} because container already has {_DependencyName} registered.")
            return getattr(serviceProvider, _DependencyName) # perhaps this should raise an exception because you shouldn't have two classes with the same namespace

        # Get DI parameters from constructor
        #   If there aren't any, register this class
        #   Otherwise recall this method for each DI parameter, then register this class
        _DependencyParametersFromConstructor = [_Param for _ParamName, _Param in inspect.signature(classType.__init__).parameters.items()
                                            if _ParamName.startswith("DI_") and _Param.annotation != inspect.Parameter.empty]

        if not _DependencyParametersFromConstructor:
            setattr(serviceProvider, _DependencyName, providers.Factory(classType))
            return getattr(serviceProvider, _DependencyName)

        _SubDependencies = []
        for _Dependency in _DependencyParametersFromConstructor:
            _SubDependencies.append(ServiceProviderExtensions.RegisterDependency(serviceProvider, _Dependency.name, _Dependency.annotation, interfaceRegistry))

        setattr(
            serviceProvider,
            _DependencyName,
            providers.Factory(
                classType,
                *_SubDependencies
            )
        )
        return getattr(serviceProvider, _DependencyName)


    """
    WORKING VERSION OF RECURSIVE REGISTER

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
                    constructor_params = inspect.signature(type.__init__).parameters
                    subDependencies = []

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
                    
                    # TODO: Investigate if this won't work if the class to be registered does not match file name

        v = ServiceProviderExtensions.GetService(serviceProvider, CreateTestEntityInteractor)
        valid_input_port = CreateTestEntityInputPort("Hello")
        output_port = CreateTestEntityPresenter()
        v.Execute(valid_input_port, output_port)
        vb = 0

    @staticmethod
    def RecursiveRegister(serviceProvider, className, classType, interfaceRegistry): #TODO: type is actually class though, might need to call it 'cls'
        _IsInterface = ABC in classType.__bases__

        if _IsInterface and classType not in [interfaceConcretePair[0] for interfaceConcretePair in interfaceRegistry]:
            raise LookupError(f"Interface '{classType.__name__}' does not have a concrete class registered.")

        if _IsInterface:
            classType = [interfaceConcretePair[1] for interfaceConcretePair in interfaceRegistry if interfaceConcretePair[0] == classType][0]

        _ConstructorParams = inspect.signature(classType.__init__).parameters.items()

        _TypeMatch = re.search(r"(?<=')[^']+(?=')", str(classType))

        if not _TypeMatch: #TODO: investigate if this is even necessary
            raise Exception(f"Could not detect class from fully qualified name of {classType}.")

        _DependencyName = _TypeMatch.group().replace('.', '_')
        #_DependencyName = "".join([string.capitalize() for string in re.findall("[A-Za-z][a-z]*", _TypeMatch.group())])

        if not any(_ParamName.startswith("DI_") for _ParamName, _Param in _ConstructorParams):
            # TODO: This could...potentially be a GetOrCreate method
            return ServiceProviderExtensions.RegisterDependency(serviceProvider, _DependencyName, classType, interfaceRegistry, None) #TODO: must be a better way to pass interfaceRegistry

        _SubDependencies = [param for paramName, param in _ConstructorParams if paramName.startswith("DI_") and param.annotation != inspect.Parameter.empty]

        _SubDependencyNames = []
        for _SubDependency in _SubDependencies:
            xyz = ServiceProviderExtensions.RecursiveRegister(serviceProvider, _SubDependency.name, _SubDependency.annotation, interfaceRegistry)
            _SubDependencyNames.append(xyz)

        return ServiceProviderExtensions.RegisterDependency(serviceProvider, _DependencyName, classType, interfaceRegistry, _SubDependencyNames)


    @staticmethod
    def RegisterDependency(serviceProvider, name: str, type: type, interfaceRegistry: List[Tuple[type, type]], subDependencies: List[type]): # TODO: Confirm if correct type hints
        members = inspect.getmembers(serviceProvider)
        for member in members:
            _MemberMatch = re.search(r"'([^']*)'", str(member[1]))
            _TypeMatch = re.search(r"'([^']*)'", str(type))
            if _MemberMatch and _TypeMatch and _MemberMatch.group(1) == _TypeMatch.group(1):
                print(f"Skipped registering '{name}' of type {type} because '{member[1]}' is already registered to {member[0]}.") # TODO: Could be logged
                return
                # TODO: PROBLEM - Outside code thinks it succeeds anyways

        if hasattr(serviceProvider, name):
            print(f"Skipped registering {name} of type {type} because container already has {name} registered.")
            return getattr(serviceProvider, name)

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

        return getattr(serviceProvider, name)
    """

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
