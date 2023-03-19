from abc import ABC
from typing import Generic

from ....Domain.Infrastructure.Generics import TOutputPort

class IInputPort(Generic[TOutputPort], ABC):
    pass
