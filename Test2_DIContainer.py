from abc import ABCMeta, abstractmethod
from dependency_injector import containers, providers

class IPersistence(metaclass=ABCMeta):
    @abstractmethod
    def Add(self) -> None:
        pass

class Persistence(IPersistence):
    def Add(self) -> None:
        print(1)

class Interactor():
    def __init__(self, persistence: IPersistence):
        self._persistence = persistence
    
    def handle(self):
        self._persistence.Add(self)

class Container(containers.DeclarativeContainer):
    dependency = providers.Object(Persistence)
    my_class = providers.Factory(Interactor, persistence=dependency)


container = Container()
interactor = container.my_class()

interactor.handle()

#Interactor(Persistence()).handle() (requires you don't put "self" as a parameter in "_persistence.Add()")