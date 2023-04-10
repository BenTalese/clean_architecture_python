from abc import ABC, abstractmethod

class IAuthenticationOutputPort(ABC):
    
    @abstractmethod
    def present_unauthenticated() -> None:
        pass
    