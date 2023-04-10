from abc import ABC, abstractmethod

class IAuthenticationOutputPort(ABC):
    
    @abstractmethod
    def PresentUnauthenticated() -> None:
        pass
    