from abc import ABC
import importlib
import inspect
import os
import sys
from Application.Infrastructure.Pipeline.INTERFACE_LOOKUP import INTERFACE_TO_CONCRETE
from dependency_injector import providers
from typing import List

sys.path.append(os.getcwd()) #fixes python unable to see Application.Infrastructure.etc...

class ServiceProviderExtensions:

    @staticmethod
    def GetService(serviceProvider, service: object) -> object:
        try:
            return serviceProvider.providers.get(service.__name__)()
        except Exception as e:
            print(f"Was not able to retrive '{service.__name__}' from DI container. (Original exception: {e}.)")

    # TODO: Currently this registers everything as a factory (need option to do singleton)
    @staticmethod
    def ConfigureServices(
        serviceProvider,
        usecase_scan_locations: List[str],
        scan_locations: List[str],
        directory_exclusion_list: List[str],
        file_exclusion_list: List[str]):

        #Scan services
        #Scan use cases

        for path in scan_locations:
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in directory_exclusion_list]
                files[:] = [f for f in files if f not in file_exclusion_list]
                for file in files:
                    # Get the module by name (module being the .py file), then get the class matching the module's name and that class's constructor's parameters
                    module_name = file[:-3]
                    module = importlib.import_module(f"{root.replace('/', '.')}.{module_name}", package=None)
                    module_class = getattr(module, module_name, None)
                    params = inspect.signature(module_class.__init__).parameters

                    # For each parameter in the constructor
                    dependencies = []
                    for parameter_name, parameter in params.items(): #if not kwargs, not args, not self,
                        parameter_type = parameter.annotation

                        # If the parameter has a type hint and the parameter's name starts with "DI_" 
                        if (parameter_type != inspect.Parameter.empty #could potentially check if DI_ specified but parameter is empty and then raise exception
                            and parameter_name.startswith("DI_")): #this is dumb...i think i should have a collection of "things to register", similar to scrutor in OSCAPI, and that list gets checked and if it doesn't contain the item then raise an exception (but to play devils advocate, DI_ does make the code more readable because you can see inside the class what is being DI'd and what is being passed in...food for thought...)
                            #and inspect.isclass(param.annotation) #this won't stop classes being registered when they should be passed in
                            #and name not in container.providers): #ALSO, THIS MIGHT NOT BE NECESSARY, THIS IS THE DEPENDENCIES OF THE DEPENDENCY, NOT THE ACTUAL REGISTERING OF THE DEPENDENCY # name or param.name might not work... e.g. container has "Example" where parameter is named "example"
                            
                            # If the parameter is an interface
                            if ABC in parameter_type.__bases__:

                                # If the interface is registered to a concrete class
                                if parameter_type in [x[0] for x in INTERFACE_TO_CONCRETE]:

                                    # Get concrete class and append to dependencies
                                    concrete_class = [x[1] for x in INTERFACE_TO_CONCRETE if x[0] == parameter_type][0]
                                    dependencies.append((parameter_name, concrete_class)) #probably this will append a camel-case name...
                                else:
                                    raise LookupError(f"Interface '{parameter_type.__name__}' does not have a concrete class registered.")
                            else:
                                dependencies.append((parameter_name, parameter_type))
                    
                    # For each dependency, check if the container has it registered and if not add it
                    for dependency_name, dependency_class in dependencies:
                        if not hasattr(serviceProvider, dependency_name):
                            setattr(serviceProvider, dependency_name, dependency_class)
                    
                    # Create a dictionary of dependencies to add to the class being registered (gets dependencies from container attributes)
                    dependency_dict = {
                        dependency_name: getattr(serviceProvider, dependency_name) for dependency_name, dependency_class in dependencies
                    }

                    # TODO: This is repeating code
                    # Register the class along with its dependencies
                    if ABC in module_class.__bases__:
                        # If the interface is registered to a concrete class
                        if module_class in [x[0] for x in INTERFACE_TO_CONCRETE]:
                            # Get concrete class and append to dependencies
                            concrete_class = [x[1] for x in INTERFACE_TO_CONCRETE if x[0] == module_class][0]
                            setattr(
                                serviceProvider,
                                module_name,
                                providers.Factory(concrete_class, *dependency_dict.values())
                            )
                        else:
                            raise LookupError(f"Interface '{module_class.__name__}' does not have a concrete class registered.")
                    else:
                        setattr(
                            serviceProvider,
                            module_name,
                            providers.Factory(module_class, *dependency_dict.values())
                        )
                    # TODO: Investigate if this won't work if the class to be registered does not match file name
