from Framework.Infrastructure import Persistence
from Application.Services import IPersistence

def startup():
    add_application_services()

    

def add_application_services():
    IPersistence.register(Persistence) # this is not correct, this method should be where services are registered to the DI container, not where interfaces are registered against implementations
    # also .register should only be used for virtual sub classes which this is not because IPersistence is passed into Persistence explicitly

if (__name__ == '__main__'):
    startup()