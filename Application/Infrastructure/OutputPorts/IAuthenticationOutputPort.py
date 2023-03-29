from abc import ABC, abstractmethod
from Domain.Infrastructure.Generics import TValidationFailure

class IAuthenticationOutputPort(ABC):
    
    @abstractmethod
    def PresentUnauthenticated() -> None:
        pass
    