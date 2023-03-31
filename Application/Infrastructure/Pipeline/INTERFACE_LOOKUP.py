from Application.Services.IPersistence import IPersistence
from Framework.Infrastructure.Persistence import Persistence

# TODO: Interfaces will have implementations in domain, application, framework, etc...
INTERFACE_TO_CONCRETE = [
    (IPersistence, Persistence)
]
