from Application.Services.IPersistence import IPersistence
from Framework.Infrastructure.Persistence import Persistence

INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence)
]
